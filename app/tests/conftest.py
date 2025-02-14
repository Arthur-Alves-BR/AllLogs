import copy
import uuid
import httpx
import pytest
import pytest_asyncio

from tortoise import Tortoise
from beanie import init_beanie

from app.main import app
from app.models.log import Log
from app.models.user import User
from app.core.enums import LogLevel
from app.models.company import Company
from app.core.database.settings import TORTOISE_ORM, mongo_client


# Mark all async tests
def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if pytest_asyncio.is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


# Init test databases
@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_dbs():
    test_db_models = copy.copy(TORTOISE_ORM["apps"]["models"])
    del test_db_models["default_connection"]

    nosql_db_name = f"test_db_{uuid.uuid4().hex}"
    no_sql_db = mongo_client[nosql_db_name]

    await init_beanie(database=no_sql_db, document_models=[Log])
    await Tortoise.init(db_url="sqlite://:memory:", modules=test_db_models)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()
    await mongo_client.drop_database(nosql_db_name)


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


@pytest_asyncio.fixture
async def test_log():
    return await Log(level=LogLevel.DEBUG, message="Test log", source=uuid.uuid4(), metadata={}).create()
