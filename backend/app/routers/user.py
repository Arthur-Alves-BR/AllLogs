from pydantic import UUID4
from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.schemas.auth import TokenUser
from app.core.request import AppRequest
from app.services.user import UserService
from app.schemas.user import GetUser, CreateUser, UpdateUser

Service = Annotated[UserService, Depends()]

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_me(request: AppRequest) -> TokenUser:
    return request.user


@router.get("/{id}")
async def get_user(id: UUID4, service: Service) -> GetUser:
    return await service.get_by_id(id)


@router.get("")
async def get_users(user_service: Service) -> list[GetUser]:
    return await user_service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, user_service: Service) -> GetUser:
    return await user_service.create(user.model_dump())


@router.put("/{id}")
async def update_user(id: UUID4, user: UpdateUser, user_service: Service) -> GetUser:
    return await user_service.update(id, user.model_dump(exclude_unset=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID4, user_service: Service) -> None:
    return await user_service.soft_delete(id)
