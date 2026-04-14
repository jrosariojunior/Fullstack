from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from app.models.exercise import DifficultyLevel, MathTopic, ExamSource


class ExerciseOption(BaseModel):
    id: str
    text: str


class ExerciseCreate(BaseModel):
    title: str
    statement: str
    options: Optional[List[ExerciseOption]] = None
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: DifficultyLevel
    topic: MathTopic
    subtopic: Optional[str] = None
    grade_levels: List[str]
    bloom_level: Optional[int] = None
    exam_source: ExamSource = ExamSource.original
    exam_year: Optional[int] = None


class ExerciseResponse(BaseModel):
    id: UUID
    title: str
    statement: str
    options: Optional[List[Any]]
    difficulty: DifficultyLevel
    topic: MathTopic
    subtopic: Optional[str]
    grade_levels: List[str]
    bloom_level: Optional[int]
    exam_source: ExamSource
    exam_year: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseAttemptCreate(BaseModel):
    exercise_id: UUID
    answer: str
    time_spent_seconds: Optional[int] = None


class ExerciseAttemptResponse(BaseModel):
    id: UUID
    exercise_id: UUID
    answer: str
    is_correct: bool
    correct_answer: str
    explanation: Optional[str]
    xp_earned: int
    created_at: datetime
