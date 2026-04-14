from fastapi import APIRouter
from app.api.v1 import auth, users, exercises, diagnostics, gamification

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(exercises.router)
router.include_router(diagnostics.router)
router.include_router(gamification.router)
