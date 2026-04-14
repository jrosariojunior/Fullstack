from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, Enum as SAEnum, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class DifficultyLevel(str, enum.Enum):
    below_basic = "abaixo_basico"
    basic = "basico"
    adequate = "adequado"
    advanced = "avancado"


class MathTopic(str, enum.Enum):
    numeros = "numeros_e_operacoes"
    algebra = "algebra"
    geometria = "geometria"
    estatistica = "estatistica_e_probabilidade"
    grandezas = "grandezas_e_medidas"
    logica = "raciocinio_logico"


class ExamSource(str, enum.Enum):
    ita = "ITA"
    fuvest = "FUVEST"
    unicamp = "UNICAMP"
    enem = "ENEM"
    fatec = "FATEC"
    etec = "ETEC"
    federal = "Instituto Federal"
    original = "Original"


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    statement = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)       # [{"id": "a", "text": "..."}]
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(SAEnum(DifficultyLevel), nullable=False)
    topic = Column(SAEnum(MathTopic), nullable=False)
    subtopic = Column(String, nullable=True)
    grade_levels = Column(JSON, default=list)  # ["6ano", "7ano"]
    bloom_level = Column(Integer, nullable=True)  # 1-6 (Bloom's Taxonomy)
    exam_source = Column(SAEnum(ExamSource), default=ExamSource.original)
    exam_year = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    attempts = relationship("ExerciseAttempt", back_populates="exercise")


class ExerciseAttempt(Base):
    __tablename__ = "exercise_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False)
    answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_spent_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="attempts")
    exercise = relationship("Exercise", back_populates="attempts")
