"""
PostgreSQL Driver - Camada de persistência com PostgreSQL.

Armazena histórico de execuções, outputs de agentes, debates,
lições aprendidas e logging completo.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
import json


Base = declarative_base()


class ExecutionModel(Base):
    """Modelo para armazenar execuções."""
    __tablename__ = "executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    briefing = Column(Text, nullable=False)
    status = Column(String(50), default="queued")  # queued, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    final_output = Column(JSONB, nullable=True)
    total_tokens = Column(Integer, default=0)

    # Relacionamentos
    agent_outputs = relationship("AgentOutputModel", back_populates="execution")
    debates = relationship("DebateModel", back_populates="execution")
    logs = relationship("ExecutionLogModel", back_populates="execution")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "briefing": self.briefing,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "final_output": self.final_output,
            "total_tokens": self.total_tokens
        }


class AgentOutputModel(Base):
    """Modelo para outputs dos agentes."""
    __tablename__ = "agent_outputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("executions.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    output = Column(JSONB, nullable=False)
    tokens_used = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relacionamento
    execution = relationship("ExecutionModel", back_populates="agent_outputs")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "execution_id": str(self.execution_id),
            "agent_name": self.agent_name,
            "output": self.output,
            "tokens_used": self.tokens_used,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


class DebateModel(Base):
    """Modelo para debates entre agentes."""
    __tablename__ = "debates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("executions.id"), nullable=False)
    round_num = Column(Integer, nullable=False)
    topic = Column(Text, nullable=False)
    positions = Column(JSONB, nullable=False)  # {agent_name: position}
    resolution = Column(Text, nullable=True)
    resolved = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relacionamento
    execution = relationship("ExecutionModel", back_populates="debates")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "execution_id": str(self.execution_id),
            "round": self.round_num,
            "topic": self.topic,
            "positions": self.positions,
            "resolution": self.resolution,
            "resolved": self.resolved,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


class LessonLearnedModel(Base):
    """Modelo para lições aprendidas (memória longo prazo)."""
    __tablename__ = "lessons_learned"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern = Column(String(200), nullable=False)  # Tipo de problema
    insight = Column(Text, nullable=False)  # Lição aprendida
    created_at = Column(DateTime, default=datetime.utcnow)
    used_count = Column(Integer, default=0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "pattern": self.pattern,
            "insight": self.insight,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "used_count": self.used_count
        }


class ExecutionLogModel(Base):
    """Modelo para logging detalhado."""
    __tablename__ = "execution_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("executions.id"), nullable=False)
    log_entry = Column(JSONB, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relacionamento
    execution = relationship("ExecutionModel", back_populates="logs")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "execution_id": str(self.execution_id),
            "log_entry": self.log_entry,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


class PostgresDriver:
    """
    Driver para PostgreSQL.

    Gerencia persistência de execuções, agentes, debates e lições.
    """

    def __init__(self, database_url: str):
        """
        Inicializa driver PostgreSQL.

        Args:
            database_url: URL de conexão (postgresql://user:pass@host/db)
        """
        self.database_url = database_url
        self.engine = None
        self.async_session = None

    async def initialize(self) -> None:
        """Inicializa conexão com banco de dados."""
        self.engine = create_async_engine(
            self.database_url,
            echo=False,
            pool_size=20,
            max_overflow=0
        )

        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        # Cria tabelas
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        """Fecha conexão com banco."""
        if self.engine:
            await self.engine.dispose()

    async def save_execution(self, execution_data: Dict[str, Any]) -> str:
        """
        Salva uma execução.

        Args:
            execution_data: Dict com dados da execução

        Returns:
            ID da execução salva
        """
        async with self.async_session() as session:
            execution = ExecutionModel(
                briefing=json.dumps(execution_data.get("briefing", {})),
                status=execution_data.get("status", "running")
            )
            session.add(execution)
            await session.commit()
            return str(execution.id)

    async def update_execution_status(self, execution_id: str, status: str) -> None:
        """Atualiza status de uma execução."""
        async with self.async_session() as session:
            execution = await session.get(ExecutionModel, uuid.UUID(execution_id))
            if execution:
                execution.status = status
                if status == "completed":
                    execution.completed_at = datetime.utcnow()
                await session.commit()

    async def save_agent_output(self, execution_id: str, agent_name: str, output: Dict[str, Any]) -> None:
        """
        Salva output de um agente.

        Args:
            execution_id: ID da execução
            agent_name: Nome do agente
            output: Output estruturado
        """
        async with self.async_session() as session:
            agent_output = AgentOutputModel(
                execution_id=uuid.UUID(execution_id),
                agent_name=agent_name,
                output=output,
                tokens_used=output.get("tokens_used", 0)
            )
            session.add(agent_output)
            await session.commit()

    async def save_debate(
        self,
        execution_id: str,
        round_num: int,
        topic: str,
        positions: Dict[str, str],
        resolution: Optional[str] = None
    ) -> None:
        """Salva um debate."""
        async with self.async_session() as session:
            debate = DebateModel(
                execution_id=uuid.UUID(execution_id),
                round_num=round_num,
                topic=topic,
                positions=positions,
                resolution=resolution,
                resolved=resolution is not None
            )
            session.add(debate)
            await session.commit()

    async def save_lesson_learned(self, pattern: str, insight: str) -> None:
        """Salva lição aprendida."""
        async with self.async_session() as session:
            # Verifica se padrão já existe
            from sqlalchemy import select
            stmt = select(LessonLearnedModel).where(LessonLearnedModel.pattern == pattern)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                existing.used_count += 1
            else:
                lesson = LessonLearnedModel(pattern=pattern, insight=insight)
                session.add(lesson)

            await session.commit()

    async def save_log_entry(self, execution_id: str, log_entry: Dict[str, Any]) -> None:
        """Salva entrada de log."""
        async with self.async_session() as session:
            log = ExecutionLogModel(
                execution_id=uuid.UUID(execution_id),
                log_entry=log_entry
            )
            session.add(log)
            await session.commit()

    async def get_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Recupera uma execução."""
        async with self.async_session() as session:
            execution = await session.get(ExecutionModel, uuid.UUID(execution_id))
            return execution.to_dict() if execution else None

    async def get_execution_history(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Recupera histórico de execuções."""
        from sqlalchemy import select, desc
        async with self.async_session() as session:
            stmt = select(ExecutionModel).order_by(desc(ExecutionModel.created_at)).limit(limit).offset(offset)
            result = await session.execute(stmt)
            executions = result.scalars().all()
            return [e.to_dict() for e in executions]

    async def get_agent_outputs(self, execution_id: str) -> List[Dict[str, Any]]:
        """Recupera outputs de agentes de uma execução."""
        from sqlalchemy import select
        async with self.async_session() as session:
            stmt = select(AgentOutputModel).where(AgentOutputModel.execution_id == uuid.UUID(execution_id))
            result = await session.execute(stmt)
            outputs = result.scalars().all()
            return [o.to_dict() for o in outputs]

    async def get_debates(self, execution_id: str) -> List[Dict[str, Any]]:
        """Recupera debates de uma execução."""
        from sqlalchemy import select
        async with self.async_session() as session:
            stmt = select(DebateModel).where(DebateModel.execution_id == uuid.UUID(execution_id))
            result = await session.execute(stmt)
            debates = result.scalars().all()
            return [d.to_dict() for d in debates]

    async def get_lessons_learned(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Recupera lições aprendidas."""
        from sqlalchemy import select, desc
        async with self.async_session() as session:
            stmt = select(LessonLearnedModel).order_by(desc(LessonLearnedModel.used_count)).limit(limit)
            result = await session.execute(stmt)
            lessons = result.scalars().all()
            return [l.to_dict() for l in lessons]

    async def get_logs(self, execution_id: str) -> List[Dict[str, Any]]:
        """Recupera logs de uma execução."""
        from sqlalchemy import select, desc
        async with self.async_session() as session:
            stmt = select(ExecutionLogModel).where(
                ExecutionLogModel.execution_id == uuid.UUID(execution_id)
            ).order_by(desc(ExecutionLogModel.timestamp))
            result = await session.execute(stmt)
            logs = result.scalars().all()
            return [l.to_dict() for l in logs]

    async def finalize_execution(self, execution_id: str, final_output: Dict[str, Any], total_tokens: int) -> None:
        """Finaliza uma execução."""
        async with self.async_session() as session:
            execution = await session.get(ExecutionModel, uuid.UUID(execution_id))
            if execution:
                execution.status = "completed"
                execution.completed_at = datetime.utcnow()
                execution.final_output = final_output
                execution.total_tokens = total_tokens
                await session.commit()

    async def search_executions(self, status: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Busca execuções por status."""
        from sqlalchemy import select, desc
        async with self.async_session() as session:
            if status:
                stmt = select(ExecutionModel).where(
                    ExecutionModel.status == status
                ).order_by(desc(ExecutionModel.created_at)).limit(limit)
            else:
                stmt = select(ExecutionModel).order_by(desc(ExecutionModel.created_at)).limit(limit)

            result = await session.execute(stmt)
            executions = result.scalars().all()
            return [e.to_dict() for e in executions]
