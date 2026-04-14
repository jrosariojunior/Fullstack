"""
Route: /history - Histórico de execuções.
"""

import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from backend.api.schemas import HistoryResponseSchema, ExecutionSummarySchema
from backend.storage import StorageManager

router = APIRouter()


@router.get("/history", response_model=HistoryResponseSchema)
async def get_history(
    limit: int = Query(20, ge=1, le=100, description="Limite de registros por página"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    status: str = Query(None, description="Filtrar por status (queued, running, completed, failed)"),
    storage: StorageManager = Depends(lambda: None)
) -> HistoryResponseSchema:
    """
    Retorna histórico de execuções com paginação.

    Inclui resumo de cada execução para visualização rápida.

    **Query Parameters:**
    - `limit`: Número de registros (padrão: 20, máx: 100)
    - `offset`: Offset para paginação (padrão: 0)
    - `status`: Filtrar por status (opcional)

    **Status Possíveis:**
    - `queued`: Aguardando
    - `running`: Em execução
    - `completed`: Completa
    - `failed`: Falhou

    **Exemplo de Response:**
    ```json
    {
      "total": 1234,
      "limit": 20,
      "offset": 0,
      "executions": [
        {
          "execution_id": "550e8400-e29b-41d4-a716-446655440000",
          "briefing_summary": "Sistema de e-commerce escalável...",
          "status": "completed",
          "created_at": "2025-01-15T10:30:00Z",
          "completed_at": "2025-01-15T10:35:00Z",
          "tokens_used": 15000,
          "agents_completed": 5,
          "total_agents": 6
        },
        ...
      ]
    }
    ```
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Recupera histórico
        if status:
            executions = await storage.search_executions(status=status, limit=limit + offset)
            # Aplica paginação manual
            executions = executions[offset:offset + limit]
        else:
            executions = await storage.get_execution_history(limit=limit, offset=offset)

        # Converte para summaries
        summaries = []
        for execution in executions:
            try:
                briefing = json.loads(execution["briefing"]) if isinstance(execution["briefing"], str) else execution["briefing"]
                summary = ExecutionSummarySchema(
                    execution_id=execution["id"],
                    briefing_summary=briefing.get("description", "")[:100],
                    status=execution["status"],
                    created_at=execution["created_at"],
                    completed_at=execution.get("completed_at"),
                    tokens_used=execution.get("total_tokens", 0),
                    agents_completed=5,  # Simplificado
                    total_agents=6
                )
                summaries.append(summary)
            except Exception:
                continue

        # Total (simplificado)
        total = len(summaries)

        return HistoryResponseSchema(
            total=total,
            limit=limit,
            offset=offset,
            executions=summaries
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao recuperar histórico: {str(e)}"
        )


@router.get("/history/stats")
async def get_history_stats(
    days: int = Query(30, ge=1, le=365, description="Últimos N dias"),
    storage: StorageManager = Depends(lambda: None)
):
    """
    Retorna estatísticas de histórico (agregado).

    Útil para dashboards e análise de tendências.

    **Query Parameters:**
    - `days`: Últimos N dias para análise (padrão: 30)

    **Exemplo de Response:**
    ```json
    {
      "total_executions": 1234,
      "completed": 1100,
      "failed": 34,
      "in_progress": 100,
      "success_rate": 0.9275,
      "avg_tokens_per_execution": 12500,
      "total_tokens_processed": 15312500,
      "period_days": 30
    }
    ```
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Recupera histórico
        history = await storage.get_execution_history(limit=10000)

        # Filtra por data
        cutoff = datetime.utcnow() - timedelta(days=days)

        filtered = []
        for exec_data in history:
            try:
                created = datetime.fromisoformat(exec_data["created_at"])
                if created >= cutoff:
                    filtered.append(exec_data)
            except:
                pass

        # Calcula estatísticas
        total = len(filtered)
        completed = sum(1 for e in filtered if e["status"] == "completed")
        failed = sum(1 for e in filtered if e["status"] == "failed")
        in_progress = sum(1 for e in filtered if e["status"] in ["queued", "running"])

        total_tokens = sum(e.get("total_tokens", 0) for e in filtered)
        avg_tokens = int(total_tokens / max(1, completed)) if completed > 0 else 0

        success_rate = completed / max(1, total)

        return {
            "total_executions": total,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "success_rate": success_rate,
            "avg_tokens_per_execution": avg_tokens,
            "total_tokens_processed": total_tokens,
            "period_days": days
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular estatísticas: {str(e)}"
        )


@router.get("/history/search")
async def search_history(
    query: str = Query(..., min_length=1, description="Buscar na descrição do briefing"),
    limit: int = Query(20, ge=1, le=100),
    storage: StorageManager = Depends(lambda: None)
):
    """
    Busca histórico por query de texto.

    Busca na descrição do briefing.

    **Query Parameters:**
    - `query`: Texto para buscar (obrigatório)
    - `limit`: Número máximo de resultados (padrão: 20)

    **Nota:** Busca case-insensitive.
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Recupera histórico
        history = await storage.get_execution_history(limit=10000)

        # Filtra por query
        import json
        results = []

        for execution in history:
            try:
                briefing = json.loads(execution["briefing"]) if isinstance(execution["briefing"], str) else execution["briefing"]
                description = briefing.get("description", "").lower()

                if query.lower() in description:
                    results.append({
                        "execution_id": execution["id"],
                        "briefing_summary": description[:100],
                        "status": execution["status"],
                        "created_at": execution["created_at"],
                        "tokens_used": execution.get("total_tokens", 0)
                    })

                    if len(results) >= limit:
                        break
            except:
                continue

        return {
            "query": query,
            "results_found": len(results),
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar: {str(e)}"
        )
