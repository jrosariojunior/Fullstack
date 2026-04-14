from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Enum as SAEnum, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class DiagnosticStatus(str, enum.Enum):
    in_progress = "em_andamento"
    completed = "concluido"


class DiagnosticResult(Base):
    __tablename__ = "diagnostic_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    grade_level = Column(String, nullable=False)
    status = Column(SAEnum(DiagnosticStatus), default=DiagnosticStatus.in_progress)

    # Scores by topic (0-100)
    scores = Column(JSON, default=dict)
    # { "numeros_e_operacoes": {"score": 65, "level": "basico"}, ... }

    # Identified gaps
    gaps = Column(JSON, default=list)
    # [{"topic": "algebra", "subtopic": "equacoes", "level": "abaixo_basico", "priority": 1}]

    # Personalized learning path
    learning_path = Column(JSON, default=list)
    # [{"topic": "...", "subtopic": "...", "exercises_ids": [...], "estimated_hours": 2}]

    # Bloom's Taxonomy level per topic
    bloom_levels = Column(JSON, default=dict)

    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    overall_score = Column(Float, nullable=True)
    overall_level = Column(String, nullable=True)

    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="diagnostic_results")
