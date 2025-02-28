from pydantic import UUID4
from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.services.company import CompanyService
from app.schemas.company import GetCompany, CreateCompany, UpdateCompany

Service = Annotated[CompanyService, Depends()]

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{id}")
async def get_company(id: UUID4, service: Service) -> GetCompany:
    return await service.get_by_id(id)


@router.get("")
async def get_companies(service: Service) -> list[GetCompany]:
    return await service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(company: CreateCompany, service: Service) -> GetCompany:
    return await service.create(company.model_dump())


@router.put("/{id}")
async def update_company(id: UUID4, company: UpdateCompany, service: Service) -> GetCompany:
    return await service.update(id, company.model_dump(exclude_unset=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(id: UUID4, service: Service) -> None:
    return await service.soft_delete(id)
