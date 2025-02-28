from motor.motor_asyncio import AsyncIOMotorClient
from tortoise.contrib.fastapi import RegisterTortoise

from app.core.settings import config


TORTOISE_ORM = {
    "connections": {"default": config.postgres_url},
    "apps": {
        "models": {
            "models": ["aerich.models", "app.models"],
            "default_connection": "default",
        },
    },
}

tortoise_orm = RegisterTortoise(config=TORTOISE_ORM)

mongo_client = AsyncIOMotorClient(config.mongo_url)
