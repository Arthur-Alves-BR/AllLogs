from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, UUID4

from app.core.enums import LogLevel


class GetLog(BaseModel):
    id: PydanticObjectId
    timestamp: datetime
    level: LogLevel
    message: str
    source: UUID4
    metadata: dict | None


class CreateLog(BaseModel):
    level: LogLevel
    message: str
    source: UUID4
    metadata: dict | None = None
