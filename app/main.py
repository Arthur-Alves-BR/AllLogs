from beanie import init_beanie
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.models.log import Log
from app.core.auth.user import get_current_user
from app.core.database.settings import tortoise_orm, mongo_client
from app.routers import healthcheck, application, company, user, log, auth


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    await tortoise_orm.init_orm()
    await init_beanie(database=mongo_client.all_logs, document_models=[Log])
    yield
    await tortoise_orm.close_orm()


app = FastAPI(lifespan=lifespan)

open_router = APIRouter(prefix="/api")
open_router.include_router(auth.router)
open_router.include_router(healthcheck.router)

closed_router = APIRouter(prefix="/api", dependencies=[Depends(get_current_user)])
closed_router.include_router(application.router)
closed_router.include_router(company.router)
closed_router.include_router(user.router)
closed_router.include_router(log.router)

app.include_router(open_router)
app.include_router(closed_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
