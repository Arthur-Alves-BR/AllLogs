from beanie import init_beanie
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.models.log import Log
from app.routers import healthcheck, company, user, log
from app.core.database.settings import tortoise_orm, mongo_client


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    await tortoise_orm.init_orm()
    await init_beanie(database=mongo_client.all_logs, document_models=[Log])
    yield
    await tortoise_orm.close_orm()


app = FastAPI(lifespan=lifespan)

main_router = APIRouter(prefix="/api")
main_router.include_router(healthcheck.router)
main_router.include_router(company.router)
main_router.include_router(user.router)
main_router.include_router(log.router)

app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
