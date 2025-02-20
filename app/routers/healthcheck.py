from typing_extensions import TypedDict
from fastapi import APIRouter

router = APIRouter(tags=["healthcheck"])


class HealthCheckResponse(TypedDict):
    status: str


@router.get("/health_check")
async def health_check() -> HealthCheckResponse:
    return {"status": "Ok"}
