from datetime import timedelta

from fastapi import HTTPException, status

from app.models.user import User
from app.core.settings import config
from app.core.request import AppRequest
from app.core.auth.jwt import create_token, decode_token
from app.schemas.auth import Token, TokenUser, RefreshTokenUser


def create_user_token(user: User) -> Token:
    return Token(
        access_token=create_token(
            data=TokenUser(
                id=str(user.id),
                name=user.name,
                email=user.email,
                company_id=str(user.company_id),
            ).model_dump(),
            expiration=timedelta(minutes=config.access_token_expire_minutes),
        ),
        refresh_token=create_token(
            RefreshTokenUser(id=str(user.id)).model_dump(),
            expiration=timedelta(minutes=config.refresh_token_expire_days),
        ),
    )


def get_current_user(authorization_token: str) -> TokenUser | None:
    try:
        return TokenUser(**decode_token(authorization_token))
    except HTTPException:
        return None


def get_current_user_from_request(request: AppRequest) -> TokenUser:
    if user := request.user:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthenticated")
