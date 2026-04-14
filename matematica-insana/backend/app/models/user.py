from sqlalchemy import Column, String, Boolean, DateTime, Enum as SAEnum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


class GradeLevel(str, enum.Enum):
    ef6 = "6ano"
    ef7 = "7ano"
    ef8 = "8ano"
    ef9 = "9ano"
    em1 = "1em"
    em2 = "2em"
    em3 = "3em"
    vestibular = "vestibular"
    concurso = "concurso"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)  # null for OAuth users
    role = Column(SAEnum(UserRole), default=UserRole.student)
    grade_level = Column(SAEnum(GradeLevel), nullable=True)
    avatar_url = Column(String, nullable=True)
    oauth_provider = Column(String, nullable=True)  # "google"
    oauth_sub = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    attempts = relationship("ExerciseAttempt", back_populates="user")
    diagnostic_results = relationship("DiagnosticResult", back_populates="user")
    gamification = relationship("UserGamification", back_populates="user", uselist=False)
