from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routers import healthcheck, company, user
from app.core.database.settings import tortoise_orm


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    await tortoise_orm.init_orm()
    yield
    await tortoise_orm.close_orm()


app = FastAPI(lifespan=lifespan)

main_router = APIRouter(prefix="/api")
main_router.include_router(healthcheck.router)
main_router.include_router(company.router)
main_router.include_router(user.router)

app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
