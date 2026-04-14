from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class UserGamification(Base):
    __tablename__ = "user_gamification"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak_days = Column(Integer, default=0)
    last_activity_date = Column(DateTime(timezone=True), nullable=True)
    total_exercises = Column(Integer, default=0)
    correct_exercises = Column(Integer, default=0)
    achievements = Column(JSON, default=list)  # ["first_exercise", "week_streak", ...]

    user = relationship("User", back_populates="gamification")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(String, primary_key=True)  # "first_exercise"
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    xp_reward = Column(Integer, default=0)
    condition_type = Column(String, nullable=False)  # "exercises_count", "streak", "score"
    condition_value = Column(Integer, nullable=False)
