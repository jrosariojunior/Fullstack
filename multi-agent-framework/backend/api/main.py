"""
Main API - FastAPI application principal.

Orquestra todas as rotas e middleware da API REST.
"""

import os
import time
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from backend.api.schemas import (
    HealthCheckResponseSchema,
    StatsResponseSchema,
    ErrorResponseSchema
)
from backend.llm import LLMFactory
from backend.storage import StorageManager
from backend.core.orchestrator import TeamOrchestrator
from backend.agents import create_all_agents
from backend.api.websocket import ConnectionManager


# ===== GLOBAL STATE =====

class AppState:
    """Estado global da aplicação."""
    storage: StorageManager = None
    llm_provider = None
    team_orchestrator: TeamOrchestrator = None
    start_time: datetime = None
    total_executions: int = 0
    completed_executions: int = 0
    failed_executions: int = 0
    total_tokens_processed: int = 0
    websocket_manager = None  # ConnectionManager para WebSocket


app_state = AppState()


# ===== LIFECYCLE =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia inicialização e shutdown da aplicação."""
    # STARTUP
    try:
        # Configuração
        postgres_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://multi_agent_user:multi_agent_pass@localhost/multi_agent_db")
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        llm_provider_name = os.getenv("LLM_PROVIDER", "claude")
        llm_api_key = os.getenv("CLAUDE_API_KEY") if llm_provider_name == "claude" else os.getenv("OPENAI_API_KEY")

        # Inicializa Storage
        app_state.storage = StorageManager(postgres_url, redis_url)
        await app_state.storage.initialize()
        print("✅ Storage inicializado")

        # Inicializa LLM Provider
        app_state.llm_provider = LLMFactory.create(
            llm_provider_name,
            api_key=llm_api_key,
            temperature=0.6
        )
        await app_state.llm_provider.validate_connection()
        print(f"✅ LLM Provider ({llm_provider_name}) inicializado")

        # Inicializa Agentes
        agents = create_all_agents(app_state.llm_provider)
        print("✅ Agentes criados")

        # Inicializa Orchestrator
        app_state.team_orchestrator = TeamOrchestrator(
            agents=agents,
            llm_provider=app_state.llm_provider
        )
        print("✅ Orchestrator inicializado")

        # Inicializa WebSocket Manager
        app_state.websocket_manager = ConnectionManager()
        print("✅ WebSocket Manager inicializado")

        # Marca tempo de início
        app_state.start_time = datetime.utcnow()
        print("✅ Aplicação iniciada com sucesso")

    except Exception as e:
        print(f"❌ Erro ao iniciar: {str(e)}")
        raise

    yield

    # SHUTDOWN
    try:
        await app_state.storage.close()
        print("✅ Storage fechado")
    except Exception as e:
        print(f"⚠️ Erro ao fechar storage: {str(e)}")


# ===== FASTAPI APP =====

app = FastAPI(
    title="Multi-Agent Framework API",
    description="API para orquestração de agentes colaborativos",
    version="1.0.0",
    lifespan=lifespan
)

# ===== MIDDLEWARE =====

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom Middleware para logging e rate limiting
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Middleware para logging de requests."""
    start_time = time.time()

    # Rate limiting
    user_id = request.client.host if request.client else "unknown"
    within_limit = await app_state.storage.check_rate_limit(user_id)

    if not within_limit:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


# ===== EXCEPTION HANDLERS =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler customizado para HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseSchema(
            error=exc.detail,
            error_code=f"HTTP_{exc.status_code}"
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções genéricas."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponseSchema(
            error="Internal server error",
            detail=str(exc),
            error_code="INTERNAL_SERVER_ERROR"
        ).dict()
    )


# ===== DEPENDENCIES =====

async def get_storage() -> StorageManager:
    """Dependency para Storage Manager."""
    if not app_state.storage:
        raise HTTPException(status_code=503, detail="Storage not initialized")
    return app_state.storage


async def get_orchestrator() -> TeamOrchestrator:
    """Dependency para Orchestrator."""
    if not app_state.team_orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    return app_state.team_orchestrator


# ===== ROTAS CORE =====

@app.get("/health", response_model=HealthCheckResponseSchema)
async def health_check(storage: StorageManager = Depends(get_storage)):
    """
    Verifica saúde da aplicação.

    Valida conexões com PostgreSQL, Redis e LLM Provider.
    """
    health = await storage.health_check()

    llm_ok = False
    try:
        llm_ok = await app_state.llm_provider.validate_connection()
    except Exception:
        pass

    return HealthCheckResponseSchema(
        status="healthy" if health["healthy"] and llm_ok else "degraded",
        postgresql=health["postgresql"],
        redis=health["redis"],
        llm_provider=llm_ok
    )


@app.get("/stats", response_model=StatsResponseSchema)
async def get_stats(storage: StorageManager = Depends(get_storage)):
    """
    Retorna estatísticas da aplicação.

    Total de execuções, tokens processados, uptime, etc.
    """
    uptime = (datetime.utcnow() - app_state.start_time).total_seconds()

    history = await storage.get_execution_history(limit=1000)
    total_executions = len(history)
    completed = sum(1 for e in history if e["status"] == "completed")
    failed = sum(1 for e in history if e["status"] == "failed")

    queue_length = await storage.get_queue_length()

    return StatsResponseSchema(
        uptime_seconds=int(uptime),
        total_executions=total_executions,
        completed_executions=completed,
        failed_executions=failed,
        total_tokens_processed=app_state.total_tokens_processed,
        avg_tokens_per_execution=int(app_state.total_tokens_processed / max(1, total_executions)),
        queue_length=queue_length
    )


@app.get("/")
async def root():
    """Root endpoint com documentação."""
    return {
        "message": "Multi-Agent Framework API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "execute": "POST /execute",
            "status": "GET /status/{execution_id}",
            "result": "GET /result/{execution_id}",
            "history": "GET /history",
            "health": "GET /health",
            "stats": "GET /stats"
        }
    }


# ===== OPENAPI =====

def custom_openapi():
    """Schema OpenAPI customizado."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Multi-Agent Framework API",
        version="1.0.0",
        description="Framework para orquestração de agentes colaborativos",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ===== IMPORTAR ROTAS =====

# Importa rotas de submódulos
from backend.api.routes import execute, status_route, result, history

app.include_router(execute.router, prefix="/api", tags=["execution"])
app.include_router(status_route.router, prefix="/api", tags=["execution"])
app.include_router(result.router, prefix="/api", tags=["execution"])
app.include_router(history.router, prefix="/api", tags=["execution"])


# ===== WEBSOCKET =====

@app.websocket("/ws/{execution_id}")
async def websocket_endpoint(websocket: WebSocket, execution_id: str):
    """
    WebSocket endpoint para monitoramento em tempo real.

    Conecta cliente ao stream de atualizações de uma execução.

    **URL:** `ws://localhost:8000/ws/{execution_id}`

    **Mensagens Recebidas:**
    - `ping`: Cliente envia ping, server responde com pong
    - `get_status`: Cliente solicita status atual da execução

    **Mensagens Enviadas:**
    - `initial`: Status inicial ao conectar
    - `progress`: Atualização de progresso
    - `agent_update`: Status de agente (running, completed, failed)
    - `debate`: Atualização de debate
    - `complete`: Execução concluída
    - `error`: Erro durante execução
    - `heartbeat`: Keepalive para manter conexão
    - `pong`: Resposta a ping
    - `status`: Status atual (resposta a get_status)
    """
    from backend.api.websocket import websocket_endpoint as ws_handler

    await ws_handler(
        websocket=websocket,
        execution_id=execution_id,
        manager=app_state.websocket_manager,
        storage=app_state.storage
    )


# ===== DEBUG =====

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
