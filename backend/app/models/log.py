import pymongo

from beanie import Document
from pydantic import Field, UUID4
from datetime import datetime, UTC

from app.core.enums import LogLevel


class Log(Document):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    level: LogLevel
    message: str
    source: UUID4
    metadata: dict | None = None

    class Settings:
        name = "logs"
        indexes = [
            "level",
            "source",
            [("source", pymongo.DESCENDING), ("timestamp", pymongo.DESCENDING)],
        ]
