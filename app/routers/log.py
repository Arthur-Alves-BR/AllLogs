from beanie import PydanticObjectId
from fastapi import APIRouter, status

from app.models.log import Log
from app.schemas.log import CreateLog, GetLog

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/{id}")
async def get_log(id: PydanticObjectId) -> GetLog:
    return await Log.get(id)


@router.get("")
async def get_logs() -> list[GetLog]:
    return await Log.find_all().to_list()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_log(data: CreateLog) -> GetLog:
    return await Log(**data.model_dump()).create()
