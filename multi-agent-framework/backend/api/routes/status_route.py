"""
Route: /status/{execution_id} - Status em tempo real da execução.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from backend.api.schemas import StatusResponseSchema
from backend.storage import StorageManager
from datetime import datetime

router = APIRouter()


@router.get("/status/{execution_id}", response_model=StatusResponseSchema)
async def get_status(
    execution_id: str,
    include_queue: bool = Query(True, description="Incluir posição na fila?"),
    storage: StorageManager = Depends(lambda: None)
) -> StatusResponseSchema:
    """
    Retorna status em tempo real de uma execução.

    Valida se execução existe e retorna progresso atual.

    **Query Parameters:**
    - `include_queue`: Incluir posição na fila (padrão: true)

    **Status Possíveis:**
    - `queued`: Aguardando processamento
    - `running`: Em execução
    - `completed`: Concluída com sucesso
    - `failed`: Falhou

    **Fases Possíveis:**
    - `initialization`: Inicializando
    - `parallel_analysis`: Analisando em paralelo
    - `conflict_detection`: Detectando conflitos
    - `debate`: Debatendo
    - `synthesis`: Sintetizando
    - `humanization`: Humanizando
    - `completion`: Finalizando

    **Exemplo de Response:**
    ```json
    {
      "execution_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "running",
      "progress": {
        "total_agents": 6,
        "completed_agents": 3,
        "percentage": 50
      },
      "agents_status": {
        "Architect": "completed",
        "Analyst": "completed",
        "Developer": "running",
        "TechReviewer": "pending",
        "QAEngineer": "pending"
      },
      "current_phase": "parallel_analysis",
      "estimated_completion": "2025-01-15T10:35:00Z"
    }
    ```
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Tenta recuperar do Redis (cache)
        context = await storage.get_context(execution_id)

        if not context:
            # Fallback para PostgreSQL
            execution = await storage.get_execution(execution_id)
            if not execution:
                raise HTTPException(
                    status_code=404,
                    detail=f"Execução {execution_id} não encontrada"
                )

            # Construir context do PostgreSQL
            context = execution

        status = context.get("status", "unknown")

        # Recupera outputs completados dos agentes
        completed_outputs = await storage.get_agent_outputs(execution_id)
        completed_agent_names = {output["agent_name"] for output in completed_outputs}

        agents_status = {}
        for agent_name in ["Architect", "Analyst", "Developer", "TechReviewer", "QAEngineer"]:
            if agent_name in completed_agent_names:
                agents_status[agent_name] = "completed"
            else:
                agents_status[agent_name] = "pending"

        # Calcula progresso
        completed = sum(1 for s in agents_status.values() if s == "completed")
        total = len(agents_status)
        percentage = int((completed / total) * 100) if total > 0 else 0

        # Posição na fila
        queue_position = None
        if status == "queued" and include_queue:
            queue_position = 1  # Simplificado, em produção seria mais complexo

        # Retorna response
        return StatusResponseSchema(
            execution_id=execution_id,
            status=status,
            progress={
                "total_agents": total,
                "completed_agents": completed,
                "percentage": percentage
            },
            agents_status=agents_status,
            current_phase=context.get("current_phase"),
            estimated_completion=None,  # Calculado na execução
            queue_position=queue_position
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao recuperar status: {str(e)}"
        )


@router.get("/status/{execution_id}/agents")
async def get_execution_agents(
    execution_id: str,
    agent_name: str = Query(None, description="Filtrar por agente específico"),
    storage: StorageManager = Depends(lambda: None)
):
    """
    Retorna detalhes dos agentes de uma execução.

    Útil para monitoramento detalhado de progresso.

    **Query Parameters:**
    - `agent_name`: Filtrar por agente específico (opcional)
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Recupera outputs dos agentes
        outputs = await storage.get_agent_outputs(execution_id)

        if agent_name:
            # Filtrar por agente
            for output in outputs:
                if output["agent_name"] == agent_name:
                    return {"agent": agent_name, "output": output}

            raise HTTPException(
                status_code=404,
                detail=f"Agente {agent_name} não encontrado"
            )

        # Retorna todos
        return {"agents": {output["agent_name"]: output for output in outputs}}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao recuperar agentes: {str(e)}"
        )
