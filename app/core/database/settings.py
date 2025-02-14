from motor.motor_asyncio import AsyncIOMotorClient
from tortoise.contrib.fastapi import RegisterTortoise


TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres:password@localhost/app"},
    "apps": {
        "models": {
            "models": ["aerich.models", "app.models.user", "app.models.company"],
            "default_connection": "default",
        },
    },
}

tortoise_orm = RegisterTortoise(config=TORTOISE_ORM)

mongo_client = AsyncIOMotorClient("mongodb://mongo:password@127.0.0.1:27017")
