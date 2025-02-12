from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class GetCompany(BaseModel):
    id: UUID4
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CreateCompany(BaseModel):
    name: str = Field(min_length=1)


class UpdateCompany(BaseModel):
    name: str = Field(min_length=1)
