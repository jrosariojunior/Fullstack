from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Matemática Insana"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/matematica_insana"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # OAuth - Google
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
