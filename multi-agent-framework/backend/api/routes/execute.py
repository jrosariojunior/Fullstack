"""
Route: /execute - Inicia execução do time de agentes.
"""

import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from backend.api.schemas import ExecuteRequestSchema, ExecuteResponseSchema
from backend.storage import StorageManager
from backend.core.orchestrator import TeamOrchestrator, ExecutionConfig


router = APIRouter()


@router.post("/execute", response_model=ExecuteResponseSchema, status_code=202)
async def execute(
    request: ExecuteRequestSchema,
    background_tasks: BackgroundTasks,
    storage: StorageManager = Depends(lambda: None),  # Será injetado do app_state
) -> ExecuteResponseSchema:
    """
    Inicia execução do time de agentes.

    Submete briefing e inicia análise colaborativa.

    **Validações:**
    - Descrição do briefing obrigatória (min 10 caracteres)
    - Token limit mínimo de 1000

    **Retorno:**
    - 202 Accepted com execution_id e status_url
    - Cliente deve consultar /status/{execution_id} para acompanhar

    **Exemplo:**
    ```json
    {
      "briefing": {
        "description": "Quero um sistema de e-commerce escalável...",
        "requirements": [
          {
            "type": "functional",
            "description": "Carrinho de compras",
            "priority": "must"
          }
        ]
      },
      "parallel": true,
      "max_debate_rounds": 3,
      "token_limit": 100000
    }
    ```
    """
    # Injeta app state (workaround para dependency injection)
    from backend.api.main import app_state

    storage = app_state.storage
    orchestrator = app_state.team_orchestrator

    if not storage or not orchestrator:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Inicia execução no storage
        execution_id = await storage.start_execution(request.briefing.dict())

        # Cria configuração
        config = ExecutionConfig(
            parallel=request.parallel,
            max_debate_rounds=request.max_debate_rounds,
            token_limit=request.token_limit,
            humanize_output=request.humanize_output
        )

        # Enfileira execução para processamento em background
        await storage.enqueue_execution({
            "execution_id": execution_id,
            "briefing": request.briefing.dict(),
            "config": {
                "parallel": config.parallel,
                "max_debate_rounds": config.max_debate_rounds,
                "token_limit": config.token_limit,
                "humanize_output": config.humanize_output
            },
            "llm_provider": request.llm_provider,
            "llm_model": request.llm_model
        })

        # Executa em background
        background_tasks.add_task(
            _execute_orchestration,
            execution_id=execution_id,
            briefing=request.briefing.dict(),
            config=config,
            orchestrator=orchestrator,
            storage=storage,
            app_state=app_state
        )

        return ExecuteResponseSchema(
            execution_id=execution_id,
            status="queued",
            estimated_duration="2-5 minutes",
            status_url=f"/api/status/{execution_id}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao iniciar execução: {str(e)}"
        )


async def _execute_orchestration(
    execution_id: str,
    briefing: dict,
    config: ExecutionConfig,
    orchestrator: TeamOrchestrator,
    storage: StorageManager,
    app_state
) -> None:
    """
    Executa orquestração em background.

    Processa todos os agentes, facilita debate e gera resultado.
    """
    try:
        # Marca como running
        await storage.postgres.update_execution_status(execution_id, "running")

        # Log de início
        await storage.log_event(execution_id, {
            "phase": "initialization",
            "message": "Iniciando execução"
        })

        # Executa orchestrator
        result = await orchestrator.execute(
            briefing=briefing
        )

        # Atualiza tokens
        app_state.total_tokens_processed += result.total_tokens_used

        # Salva resultado
        await storage.finalize_execution(
            execution_id=execution_id,
            final_output=result.final_output,
            total_tokens=result.total_tokens_used
        )

        # Log de sucesso
        await storage.log_event(execution_id, {
            "phase": "completion",
            "status": "success",
            "total_tokens": result.total_tokens_used
        })

        app_state.completed_executions += 1

    except Exception as e:
        # Log de erro
        await storage.log_event(execution_id, {
            "phase": "error",
            "error": str(e)
        })

        # Marca como failed
        await storage.postgres.update_execution_status(execution_id, "failed")
        app_state.failed_executions += 1

    finally:
        # Remove da fila
        await storage.dequeue_execution()
