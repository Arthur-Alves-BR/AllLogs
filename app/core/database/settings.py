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
