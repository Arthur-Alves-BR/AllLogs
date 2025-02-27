from fastapi import APIRouter, HTTPException, status

from app.models.user import User
from app.core.auth.jwt import decode_token
from app.core.auth.user import create_user_token
from app.core.auth.password import verify_password
from app.schemas.auth import LoginData, RefreshTokenUser, Token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def token(login_data: LoginData) -> Token:
    user = await User.get_or_none(email=login_data.email)
    if not user or not verify_password(plain_password=login_data.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return create_user_token(user)


@router.post("/refresh")
async def refresh(refresh_token: str) -> Token:
    refresh_token_user = RefreshTokenUser(**decode_token(refresh_token))
    user = await User.get_or_none(id=refresh_token_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return create_user_token(user)
