from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.models.diagnostic import DiagnosticResult, DiagnosticStatus
from app.models.exercise import Exercise, ExerciseAttempt, DifficultyLevel, MathTopic
from app.schemas.diagnostic import DiagnosticStartRequest, DiagnosticAnswerRequest, DiagnosticResultResponse
from app.api.v1.users import get_current_user
from app.models.user import User
import random

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])

QUESTIONS_PER_TOPIC = 3
BLOOM_LEVELS = {
    DifficultyLevel.below_basic: 1,
    DifficultyLevel.basic: 2,
    DifficultyLevel.adequate: 3,
    DifficultyLevel.advanced: 5,
}
LEVEL_THRESHOLDS = {
    "abaixo_basico": (0, 39),
    "basico": (40, 59),
    "adequado": (60, 79),
    "avancado": (80, 100),
}


def score_to_level(score: float) -> str:
    for level, (low, high) in LEVEL_THRESHOLDS.items():
        if low <= score <= high:
            return level
    return "abaixo_basico"


@router.post("/start", response_model=DiagnosticResultResponse, status_code=201)
def start_diagnostic(
    data: DiagnosticStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    diagnostic = DiagnosticResult(
        user_id=current_user.id,
        grade_level=data.grade_level,
        status=DiagnosticStatus.in_progress,
    )
    db.add(diagnostic)
    db.commit()
    db.refresh(diagnostic)
    return diagnostic


@router.post("/answer", response_model=DiagnosticResultResponse)
def submit_diagnostic_answer(
    data: DiagnosticAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    diagnostic = db.query(DiagnosticResult).filter(
        DiagnosticResult.id == data.diagnostic_id,
        DiagnosticResult.user_id == current_user.id,
    ).first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnóstico não encontrado")
    if diagnostic.status == DiagnosticStatus.completed:
        raise HTTPException(status_code=400, detail="Diagnóstico já concluído")

    exercise = db.query(Exercise).filter(Exercise.id == data.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    is_correct = data.answer.strip().lower() == exercise.correct_answer.strip().lower()

    scores = diagnostic.scores or {}
    topic = exercise.topic.value
    if topic not in scores:
        scores[topic] = {"correct": 0, "total": 0}
    scores[topic]["total"] += 1
    if is_correct:
        scores[topic]["correct"] += 1

    diagnostic.scores = scores
    diagnostic.total_questions = (diagnostic.total_questions or 0) + 1
    if is_correct:
        diagnostic.correct_answers = (diagnostic.correct_answers or 0) + 1

    db.commit()
    db.refresh(diagnostic)
    return diagnostic


@router.post("/{diagnostic_id}/complete", response_model=DiagnosticResultResponse)
def complete_diagnostic(
    diagnostic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    diagnostic = db.query(DiagnosticResult).filter(
        DiagnosticResult.id == diagnostic_id,
        DiagnosticResult.user_id == current_user.id,
    ).first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnóstico não encontrado")

    scores = diagnostic.scores or {}
    topic_scores = {}
    gaps = []
    learning_path = []

    for topic, data in scores.items():
        if data["total"] > 0:
            pct = (data["correct"] / data["total"]) * 100
            level = score_to_level(pct)
            topic_scores[topic] = {"score": round(pct, 1), "level": level}

            if pct < 60:
                gaps.append({"topic": topic, "score": pct, "level": level, "priority": 1 if pct < 40 else 2})
                learning_path.append({"topic": topic, "level": level, "priority": 1 if pct < 40 else 2, "estimated_hours": 4 if pct < 40 else 2})

    overall = (diagnostic.correct_answers / diagnostic.total_questions * 100) if diagnostic.total_questions > 0 else 0

    diagnostic.scores = topic_scores
    diagnostic.gaps = sorted(gaps, key=lambda x: x["priority"])
    diagnostic.learning_path = sorted(learning_path, key=lambda x: x["priority"])
    diagnostic.overall_score = round(overall, 1)
    diagnostic.overall_level = score_to_level(overall)
    diagnostic.status = DiagnosticStatus.completed
    diagnostic.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(diagnostic)
    return diagnostic


@router.get("/", response_model=List[DiagnosticResultResponse])
def list_diagnostics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(DiagnosticResult).filter(DiagnosticResult.user_id == current_user.id).all()


@router.get("/{diagnostic_id}", response_model=DiagnosticResultResponse)
def get_diagnostic(
    diagnostic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    diagnostic = db.query(DiagnosticResult).filter(
        DiagnosticResult.id == diagnostic_id,
        DiagnosticResult.user_id == current_user.id,
    ).first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnóstico não encontrado")
    return diagnostic
