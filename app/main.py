from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from .routers import healthcheck


app = FastAPI()

app.include_router(healthcheck.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


register_tortoise(
    app,
    db_url="postgres://postgres:password@localhost/app",
    modules={"models": ["app.models.user"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
