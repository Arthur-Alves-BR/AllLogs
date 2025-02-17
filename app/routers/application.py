from pydantic import UUID4
from fastapi import APIRouter, status

from app.services import application_service
from app.schemas.application import GetApplication, CreateApplication, UpdateApplication

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("/{id}")
async def get_application(id: UUID4) -> GetApplication:
    return await application_service.get_by_id(id)


@router.get("")
async def get_applications() -> list[GetApplication]:
    return await application_service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_application(user: CreateApplication) -> GetApplication:
    return await application_service.create(user.model_dump())


@router.put("/{id}")
async def update_application(id: UUID4, user: UpdateApplication) -> GetApplication:
    return await application_service.update(id, user.model_dump(exclude_unset=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(id: UUID4) -> None:
    return await application_service.soft_delete(id)
