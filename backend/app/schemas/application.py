from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class GetApplication(BaseModel):
    id: UUID4
    name: str
    is_active: bool
    description: str
    company_id: UUID4
    created_at: datetime


class CreateApplication(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field("", min_length=1)
    company_id: UUID4


class UpdateApplication(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field("", min_length=1)
