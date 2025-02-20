import jwt

from datetime import timedelta
from fastapi import HTTPException, status

from app.core.settings import config
from app.core.datetime.functions import utcnow


ALGORITHM = "HS256"


def create_token(data: dict, expiration: timedelta) -> str:
    to_encode = data.copy()
    expire = utcnow() + expiration
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, config.secret_key, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        message = "Token expired"
    except jwt.PyJWTError:
        message = "Invalid token"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)
