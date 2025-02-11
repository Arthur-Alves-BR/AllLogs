from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.jwt import get_current_user


router = APIRouter()


@router.get("/health_check")
async def health_check() -> dict[str, str]:
    return {"status": "Ok"}


@router.get("/chat")
async def get_response(current_user: Annotated[dict, Depends(get_current_user)]) -> dict[str, str]:
    return {"message": "Welcome!", "user": current_user}
