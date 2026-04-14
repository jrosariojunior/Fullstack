"""
Route: /result/{execution_id} - Resultado completo da execução.
"""

import json
import os
import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from backend.api.schemas import ResultResponseSchema
from backend.storage import StorageManager

router = APIRouter()


@router.get("/result/{execution_id}", response_model=ResultResponseSchema)
async def get_result(
    execution_id: str,
    include_logs: bool = Query(True, description="Incluir logs de execução?"),
    storage: StorageManager = Depends(lambda: None)
) -> ResultResponseSchema:
    """
    Retorna resultado completo da execução.

    Inclui outputs de agentes, debate, conflitos, resultado final e logs.

    **Status Esperados:**
    - `completed`: Execução bem-sucedida
    - `failed`: Execução falhou
    - `running`: Ainda em execução

    **Query Parameters:**
    - `include_logs`: Incluir logs detalhados (padrão: true)

    **Nota:** Execuções em progresso retornam resultado parcial.

    **Exemplo de Response:**
    ```json
    {
      "execution_id": "550e8400-e29b-41d4-a716-446655440000",
      "briefing": {
        "description": "Sistema de e-commerce..."
      },
      "status": "completed",
      "results": {
        "Architect": {
          "agent_name": "Architect",
          "output": {
            "architecture_type": "microservices",
            "components": [...]
          },
          "tokens_used": 2500
        },
        ...
      },
      "debate_log": [...],
      "conflicts": [...],
      "final_output": {...},
      "metadata": {
        "started_at": "2025-01-15T10:30:00Z",
        "completed_at": "2025-01-15T10:35:00Z",
        "total_tokens_used": 15000,
        "duration_seconds": 300
      }
    }
    ```
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Recupera execução
        execution = await storage.get_execution(execution_id)
        if not execution:
            raise HTTPException(
                status_code=404,
                detail=f"Execução {execution_id} não encontrada"
            )

        # Recupera dados da execução
        agent_outputs = await storage.get_agent_outputs(execution_id)
        debates = await storage.get_debates(execution_id)
        logs = await storage.get_execution_logs(execution_id) if include_logs else []

        # Converte para schemas
        briefing_dict = json.loads(execution["briefing"]) if isinstance(execution["briefing"], str) else execution["briefing"]

        # Calcula duração
        duration_seconds = None
        if execution.get("completed_at") and execution.get("created_at"):
            try:
                start = datetime.fromisoformat(execution["created_at"])
                end = datetime.fromisoformat(execution["completed_at"])
                duration_seconds = int((end - start).total_seconds())
            except:
                pass

        # Monta resultado
        return ResultResponseSchema(
            execution_id=execution_id,
            briefing={
                "description": briefing_dict.get("description", ""),
                "requirements": briefing_dict.get("requirements", []),
                "constraints": briefing_dict.get("constraints", []),
                "preferences": briefing_dict.get("preferences")
            },
            status=execution["status"],
            results={
                output["agent_name"]: {
                    "agent_name": output["agent_name"],
                    "agent_id": output.get("agent_id", ""),
                    "output": output["output"],
                    "timestamp": output["timestamp"],
                    "tokens_used": output["tokens_used"],
                    "confidence": output["output"].get("confidence", 0.9)
                }
                for output in agent_outputs
            },
            debate_log=[
                {
                    "round": debate["round"],
                    "topic": debate["topic"],
                    "participants": [],  # Extraído de positions
                    "positions": debate["positions"],
                    "resolution": debate["resolution"],
                    "timestamp": debate["timestamp"]
                }
                for debate in debates
            ],
            conflicts=[],  # Recuperado de debates não resolvidos
            final_output=execution.get("final_output", {}),
            execution_log=[log.get("log_entry", {}).get("message", "") for log in logs],
            metadata={
                "started_at": execution["created_at"],
                "completed_at": execution["completed_at"],
                "total_tokens_used": execution["total_tokens"],
                "duration_seconds": duration_seconds,
                "status": execution["status"]
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao recuperar resultado: {str(e)}"
        )


@router.get("/result/{execution_id}/export")
async def export_execution(
    execution_id: str,
    format: str = Query("json", description="Formato: json ou csv"),
    storage: StorageManager = Depends(lambda: None)
):
    """
    Exporta resultado da execução.

    Permite download em diferentes formatos.

    **Query Parameters:**
    - `format`: json (padrão) ou csv
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Recupera execution completa
        export_data = await storage.export_execution(execution_id)

        if format.lower() == "json":
            return JSONResponse(
                content=export_data,
                headers={
                    "Content-Disposition": f"attachment; filename=execution_{execution_id}.json"
                }
            )

        elif format.lower() == "csv":
            # Converte para CSV
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["agent", "metric", "value"])
            writer.writeheader()

            # Escreve dados
            for agent_name, agent_output in export_data.get("agent_outputs", {}).items():
                writer.writerow({
                    "agent": agent_name,
                    "metric": "tokens_used",
                    "value": agent_output.get("tokens_used", 0)
                })

            return JSONResponse(
                content={"detail": "CSV export not fully implemented yet"},
                status_code=501
            )

        else:
            raise HTTPException(status_code=400, detail="Formato não suportado")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao exportar: {str(e)}"
        )


@router.get("/result/{execution_id}/download")
async def download_result(
    execution_id: str,
    storage: StorageManager = Depends(lambda: None)
):
    """
    Download do resultado completo como arquivo JSON.
    """
    from backend.api.main import app_state

    storage = app_state.storage

    if not storage:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        # Recupera resultado
        result = await get_result(execution_id, include_logs=True, storage=storage)

        # Cria arquivo temporário
        filename = f"/tmp/execution_{execution_id}.json"
        with open(filename, "w") as f:
            json.dump(result.dict(default=str), f, indent=2)

        return FileResponse(
            path=filename,
            filename=f"execution_{execution_id}.json",
            media_type="application/json"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer download: {str(e)}"
        )
