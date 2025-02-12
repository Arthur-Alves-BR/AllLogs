import copy
import httpx
import pytest_asyncio

from app.main import app
from app.core.database.settings import TORTOISE_ORM

from tortoise import Tortoise

from app.models.user import User
from app.models.company import Company


@pytest_asyncio.fixture(scope="module", autouse=True)
async def init_db():
    test_db_models = copy.copy(TORTOISE_ORM["apps"]["models"])
    del test_db_models["default_connection"]

    await Tortoise.init(db_url="sqlite://:memory:", modules=test_db_models)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


@pytest_asyncio.fixture
async def api_client():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test/api") as client:
        yield client


@pytest_asyncio.fixture
async def test_company():
    return await Company.create(name="Test Company")


@pytest_asyncio.fixture
async def test_user(test_company):
    return await User.create(name="Test User", email="123@gmail.com", password="1234", company=test_company)  # noqa: S106
