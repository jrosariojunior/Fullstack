"""
Schemas - Modelos Pydantic para requests/responses da API.

Define estruturas de entrada e saída validadas automaticamente.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ===== ENUMS =====

class ExecutionStatus(str, Enum):
    """Status de uma execução."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ValidationStatus(str, Enum):
    """Status de validação."""
    APPROVED = "approved"
    APPROVED_WITH_CONCERNS = "approved_with_concerns"
    REJECTED = "rejected"


# ===== REQUESTS =====

class RequirementSchema(BaseModel):
    """Um requisito do sistema."""
    type: str = Field(..., description="functional ou non_functional")
    description: str = Field(..., description="Descrição do requisito")
    priority: str = Field(..., description="must, should, could, wont")


class ConstraintSchema(BaseModel):
    """Uma restrição técnica/orçamentária."""
    type: str = Field(..., description="technical, budget, time")
    description: str = Field(..., description="Descrição da restrição")


class PreferencesSchema(BaseModel):
    """Preferências do usuário."""
    tech_stack: Optional[List[str]] = Field(None, description="Tecnologias preferidas")
    architecture_style: Optional[List[str]] = Field(None, description="Estilos arquiteturais")
    other: Optional[Dict[str, Any]] = Field(None, description="Outras preferências")


class BriefingSchema(BaseModel):
    """Briefing do projeto."""
    description: str = Field(..., min_length=10, description="Descrição do projeto")
    requirements: Optional[List[RequirementSchema]] = Field(None, description="Requisitos")
    constraints: Optional[List[ConstraintSchema]] = Field(None, description="Restrições")
    preferences: Optional[PreferencesSchema] = Field(None, description="Preferências")

    @validator("description")
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Descrição não pode estar vazia")
        return v


class ExecuteRequestSchema(BaseModel):
    """Request para executar time de agentes."""
    briefing: BriefingSchema = Field(..., description="Briefing do projeto")
    parallel: bool = Field(True, description="Executar agentes em paralelo?")
    max_debate_rounds: int = Field(3, ge=1, le=10, description="Máximo de rounds de debate")
    token_limit: int = Field(100000, ge=1000, description="Limite de tokens")
    humanize_output: bool = Field(True, description="Humanizar output?")
    llm_provider: Optional[str] = Field("claude", description="Provider LLM (claude, openai)")
    llm_model: Optional[str] = Field(None, description="Modelo específico")


# ===== RESPONSES =====

class AgentOutputSchema(BaseModel):
    """Output de um agente."""
    agent_name: str
    agent_id: str
    output: Dict[str, Any]
    timestamp: datetime
    tokens_used: int
    confidence: float = Field(..., ge=0, le=1)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DebateLogSchema(BaseModel):
    """Entrada de log de debate."""
    round: int
    topic: str
    participants: List[str]
    positions: Dict[str, str]
    resolution: Optional[str] = None
    timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ConflictSchema(BaseModel):
    """Um conflito detectado."""
    id: str
    agents: List[str]
    topic: str
    positions: Dict[str, Any]
    resolved: bool
    resolution: Optional[str] = None


class ExecutionMetadataSchema(BaseModel):
    """Metadata de execução."""
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_tokens_used: int
    duration_seconds: Optional[float] = None
    status: ExecutionStatus


class ExecuteResponseSchema(BaseModel):
    """Response para /execute (202 Accepted)."""
    execution_id: str = Field(..., description="ID da execução")
    status: ExecutionStatus = Field(..., description="Status atual")
    estimated_duration: str = Field(..., description="Duração estimada")
    status_url: str = Field(..., description="URL para verificar status")

    class Config:
        schema_extra = {
            "example": {
                "execution_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "queued",
                "estimated_duration": "2-5 minutes",
                "status_url": "/status/550e8400-e29b-41d4-a716-446655440000"
            }
        }


class StatusResponseSchema(BaseModel):
    """Response para /status."""
    execution_id: str
    status: ExecutionStatus
    progress: Dict[str, Any] = Field(..., description="Progresso da execução")
    agents_status: Dict[str, str] = Field(..., description="Status de cada agente")
    current_phase: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    queue_position: Optional[int] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ResultResponseSchema(BaseModel):
    """Response para /result."""
    execution_id: str
    briefing: BriefingSchema
    status: ExecutionStatus
    results: Dict[str, AgentOutputSchema]
    debate_log: List[DebateLogSchema]
    conflicts: List[ConflictSchema]
    final_output: Dict[str, Any]
    execution_log: List[str]
    metadata: ExecutionMetadataSchema

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ExecutionSummarySchema(BaseModel):
    """Resumo de uma execução no histórico."""
    execution_id: str
    briefing_summary: str
    status: ExecutionStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    tokens_used: int
    agents_completed: int
    total_agents: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HistoryResponseSchema(BaseModel):
    """Response para /history."""
    total: int = Field(..., description="Total de execuções")
    limit: int = Field(..., description="Limit da página")
    offset: int = Field(..., description="Offset da página")
    executions: List[ExecutionSummarySchema]


class ErrorResponseSchema(BaseModel):
    """Response de erro."""
    error: str = Field(..., description="Mensagem de erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais")
    error_code: Optional[str] = Field(None, description="Código de erro")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ResolveDisciplinaryConflictSchema(BaseModel):
    """Request para resolver conflito não convergido."""
    conflict_id: str = Field(..., description="ID do conflito")
    decision: str = Field(..., description="Decisão do usuário")
    reasoning: Optional[str] = Field(None, description="Justificativa")


class HealthCheckResponseSchema(BaseModel):
    """Response para /health."""
    status: str = Field(..., description="Saúde geral")
    postgresql: bool = Field(..., description="PostgreSQL conectado?")
    redis: bool = Field(..., description="Redis conectado?")
    llm_provider: bool = Field(..., description="LLM Provider ok?")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class StatsResponseSchema(BaseModel):
    """Response para /stats."""
    uptime_seconds: int
    total_executions: int
    completed_executions: int
    failed_executions: int
    total_tokens_processed: int
    avg_tokens_per_execution: float
    queue_length: int
    redis_memory: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# ===== WEBSOCKET =====

class WebSocketMessageSchema(BaseModel):
    """Mensagem de WebSocket."""
    type: str = Field(..., description="Tipo de mensagem: progress, error, complete")
    execution_id: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
