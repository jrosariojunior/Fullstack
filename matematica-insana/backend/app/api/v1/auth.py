from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.models.user import User
from app.models.gamification import UserGamification
from app.schemas.user import UserCreate, UserLogin, TokenResponse, RefreshTokenRequest, UserResponse
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
        grade_level=data.grade_level,
    )
    db.add(user)
    db.flush()

    gamification = UserGamification(user_id=user.id)
    db.add(gamification)
    db.commit()
    db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Conta inativa")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(User).filter(User.id == payload["sub"]).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.get("/google")
def google_login():
    from authlib.integrations.starlette_client import OAuth
    # Redirect to Google OAuth consent screen
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
    )
    return RedirectResponse(google_auth_url)


@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    import httpx

    # Exchange code for token
    token_resp = httpx.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    )
    token_data = token_resp.json()
    id_token = token_data.get("id_token")
    if not id_token:
        raise HTTPException(status_code=400, detail="Falha na autenticação Google")

    # Decode Google ID token (without verification for simplicity; use google-auth in prod)
    import base64, json
    payload_b64 = id_token.split(".")[1] + "=="
    google_user = json.loads(base64.urlsafe_b64decode(payload_b64))

    email = google_user.get("email")
    name = google_user.get("name", email)
    sub = google_user.get("sub")
    avatar = google_user.get("picture")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            name=name,
            oauth_provider="google",
            oauth_sub=sub,
            avatar_url=avatar,
            is_verified=True,
        )
        db.add(user)
        db.flush()
        db.add(UserGamification(user_id=user.id))
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return RedirectResponse(
        f"{settings.FRONTEND_URL}/auth/callback"
        f"?access_token={access_token}&refresh_token={refresh_token}"
    )
