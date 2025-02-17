from pydantic import UUID4
from fastapi import APIRouter, status

from app.services import user_service
from app.schemas.user import GetUser, CreateUser, UpdateUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}")
async def get_user(id: UUID4) -> GetUser:
    return await user_service.get_by_id(id)


@router.get("")
async def get_users() -> list[GetUser]:
    return await user_service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser) -> GetUser:
    return await user_service.create(user.model_dump())


@router.put("/{id}")
async def update_user(id: UUID4, user: UpdateUser) -> GetUser:
    return await user_service.update(id, user.model_dump(exclude_unset=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID4) -> None:
    return await user_service.soft_delete(id)
