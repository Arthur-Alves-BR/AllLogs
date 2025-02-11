import os
import traceback

from datetime import timedelta

from fastapi import Cookie, HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError

from app.core.datetime.functions import utcnow


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Cookie(None)) -> dict[str, str]:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        user_email: str = payload.get("email")

        if user_id is None or user_email is None:
            raise credentials_exception

        return {"user_id": user_id, "user_email": user_email}

    except ExpiredSignatureError as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please login again."
        ) from e
    except JWTError as e:
        traceback.print_exc()
        raise credentials_exception from e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Not Authenticated") from e


def validate_user_request(token: str = Cookie(None)) -> dict[str, str]:
    session_details = get_current_user(token)
    return session_details
