import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.sessions import SessionMiddleware

from .routers import healthcheck, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(healthcheck.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "default_secret_key"))


register_tortoise(
    app,
    db_url="postgres://postgres:password@localhost/cloud",
    modules={"models": ["app.models.user"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
