from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.gamification import UserGamification, Achievement
from app.api.v1.users import get_current_user
from app.models.user import User
from uuid import UUID

router = APIRouter(prefix="/gamification", tags=["gamification"])


class GamificationResponse(BaseModel):
    user_id: UUID
    xp: int
    level: int
    streak_days: int
    total_exercises: int
    correct_exercises: int
    accuracy: float
    achievements: List[str]

    class Config:
        from_attributes = True


class RankingEntry(BaseModel):
    rank: int
    user_name: str
    xp: int
    level: int


@router.get("/me", response_model=GamificationResponse)
def get_my_gamification(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    g = db.query(UserGamification).filter(UserGamification.user_id == current_user.id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Dados de gamificação não encontrados")

    accuracy = (g.correct_exercises / g.total_exercises * 100) if g.total_exercises > 0 else 0

    return GamificationResponse(
        user_id=g.user_id,
        xp=g.xp,
        level=g.level,
        streak_days=g.streak_days,
        total_exercises=g.total_exercises,
        correct_exercises=g.correct_exercises,
        accuracy=round(accuracy, 1),
        achievements=g.achievements or [],
    )


@router.get("/ranking", response_model=List[RankingEntry])
def get_ranking(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(UserGamification, User)
        .join(User, User.id == UserGamification.user_id)
        .order_by(UserGamification.xp.desc())
        .limit(limit)
        .all()
    )
    return [
        RankingEntry(rank=i + 1, user_name=user.name, xp=g.xp, level=g.level)
        for i, (g, user) in enumerate(results)
    ]
