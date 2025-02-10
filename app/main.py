from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .routers import healthcheck

app = FastAPI()
app.include_router(healthcheck.router)

register_tortoise(
    app,
    db_url="postgres://postgres:password@localhost/cloud",
    modules={"models": ["app.models.user"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
