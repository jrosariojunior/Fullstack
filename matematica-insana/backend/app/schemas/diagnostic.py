from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from app.models.diagnostic import DiagnosticStatus


class DiagnosticStartRequest(BaseModel):
    grade_level: str


class DiagnosticAnswerRequest(BaseModel):
    diagnostic_id: UUID
    exercise_id: UUID
    answer: str
    time_spent_seconds: Optional[int] = None


class TopicScore(BaseModel):
    score: float
    level: str


class LearningPathItem(BaseModel):
    topic: str
    subtopic: str
    estimated_hours: float
    priority: int


class DiagnosticResultResponse(BaseModel):
    id: UUID
    user_id: UUID
    grade_level: str
    status: DiagnosticStatus
    scores: Dict[str, Any]
    gaps: List[Any]
    learning_path: List[Any]
    total_questions: int
    correct_answers: int
    overall_score: Optional[float]
    overall_level: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
