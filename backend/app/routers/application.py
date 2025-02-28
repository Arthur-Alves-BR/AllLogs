from pydantic import UUID4
from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.services.application import ApplicationService
from app.schemas.application import GetApplication, CreateApplication, UpdateApplication

Service = Annotated[ApplicationService, Depends()]

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("/{id}")
async def get_application(id: UUID4, service: Service) -> GetApplication:
    return await service.get_by_id(id)


@router.get("")
async def get_applications(service: Service) -> list[GetApplication]:
    return await service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_application(user: CreateApplication, service: Service) -> GetApplication:
    return await service.create(user.model_dump())


@router.put("/{id}")
async def update_application(id: UUID4, user: UpdateApplication, service: Service) -> GetApplication:
    return await service.update(id, user.model_dump(exclude_unset=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(id: UUID4, service: Service) -> None:
    return await service.soft_delete(id)
