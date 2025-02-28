from typing import Annotated
from datetime import datetime

from pydantic import AfterValidator, BaseModel, EmailStr, UUID4, Field

from app.core.auth.password import is_valid_password


class GetUser(BaseModel):
    id: UUID4
    name: str = Field(min_length=1)
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
    company_id: UUID4


class CreateUser(BaseModel):
    name: str = Field(min_length=1)
    password: Annotated[str, AfterValidator(is_valid_password)]
    email: EmailStr
    company_id: UUID4


class UpdateUser(BaseModel):
    name: str | None = Field(None, min_length=1)
    email: EmailStr | None = None
