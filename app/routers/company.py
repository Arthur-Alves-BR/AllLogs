from pydantic import UUID4
from fastapi import APIRouter, status

from app.services import company_service
from app.schemas.company import GetCompany, CreateCompany, UpdateCompany

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{id}")
async def get_company(id: UUID4) -> GetCompany:
    return await company_service.get_by_id(id)


@router.get("")
async def get_companies() -> list[GetCompany]:
    return await company_service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(company: CreateCompany) -> GetCompany:
    return await company_service.create(company.model_dump())


@router.put("/{id}")
async def update_company(id: UUID4, company: UpdateCompany) -> GetCompany:
    return await company_service.update(id, company.model_dump(exclude_unset=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(id: UUID4) -> None:
    return await company_service.soft_delete(id)
