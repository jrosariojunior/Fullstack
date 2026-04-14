from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.core.database import get_db
from app.models.exercise import Exercise, ExerciseAttempt, DifficultyLevel, MathTopic
from app.models.gamification import UserGamification
from app.schemas.exercise import ExerciseCreate, ExerciseResponse, ExerciseAttemptCreate, ExerciseAttemptResponse
from app.api.v1.users import get_current_user
from app.models.user import User

router = APIRouter(prefix="/exercises", tags=["exercises"])

XP_BY_DIFFICULTY = {
    DifficultyLevel.below_basic: 5,
    DifficultyLevel.basic: 10,
    DifficultyLevel.adequate: 20,
    DifficultyLevel.advanced: 30,
}


@router.get("/", response_model=List[ExerciseResponse])
def list_exercises(
    topic: Optional[MathTopic] = None,
    difficulty: Optional[DifficultyLevel] = None,
    grade_level: Optional[str] = None,
    limit: int = Query(default=20, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Exercise).filter(Exercise.is_active == True)
    if topic:
        query = query.filter(Exercise.topic == topic)
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)
    if grade_level:
        query = query.filter(Exercise.grade_levels.contains([grade_level]))
    return query.offset(offset).limit(limit).all()


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return exercise


@router.post("/attempt", response_model=ExerciseAttemptResponse)
def submit_attempt(
    data: ExerciseAttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise = db.query(Exercise).filter(Exercise.id == data.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    is_correct = data.answer.strip().lower() == exercise.correct_answer.strip().lower()
    xp_earned = XP_BY_DIFFICULTY[exercise.difficulty] if is_correct else 2

    attempt = ExerciseAttempt(
        user_id=current_user.id,
        exercise_id=exercise.id,
        answer=data.answer,
        is_correct=is_correct,
        time_spent_seconds=data.time_spent_seconds,
    )
    db.add(attempt)

    gamification = db.query(UserGamification).filter(UserGamification.user_id == current_user.id).first()
    if gamification:
        gamification.xp += xp_earned
        gamification.total_exercises += 1
        if is_correct:
            gamification.correct_exercises += 1
        gamification.level = max(1, gamification.xp // 100)

    db.commit()
    db.refresh(attempt)

    return ExerciseAttemptResponse(
        id=attempt.id,
        exercise_id=attempt.exercise_id,
        answer=attempt.answer,
        is_correct=is_correct,
        correct_answer=exercise.correct_answer,
        explanation=exercise.explanation,
        xp_earned=xp_earned,
        created_at=attempt.created_at,
    )


@router.post("/", response_model=ExerciseResponse, status_code=201)
def create_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.models.user import UserRole
    if current_user.role not in [UserRole.admin, UserRole.teacher]:
        raise HTTPException(status_code=403, detail="Sem permissão")

    exercise = Exercise(**data.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise
