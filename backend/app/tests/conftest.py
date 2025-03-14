import copy
import uuid
import httpx
import pytest
import pytest_asyncio

from tortoise import Tortoise
from beanie import init_beanie

from app.main import app
from app.models.log import Log
from app.models import Application, Company, User

from app.core.enums import LogLevel
from app.core.auth.user import create_user_token
from app.core.database.settings import TORTOISE_ORM, mongo_client


# Mark all async tests
def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if pytest_asyncio.is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


# Init test databases
@pytest_asyncio.fixture(scope="function", autouse=True)
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


@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_company():
    return await Company.create(name="Test Company")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_user(test_company):
    return await User.create(name="Test User", email="123@gmail.com", password="1234", company=test_company)  # noqa: S106


@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_application(test_company):
    return await Application.create(name="Test Application", description="A test app", company=test_company)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_log():
    return await Log(level=LogLevel.DEBUG, message="Test log", source=uuid.uuid4(), metadata={}).create()


@pytest_asyncio.fixture
async def api_client(test_user):
    test_token = create_user_token(test_user)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test/api",
        headers={"Authorization": f"Bearer {test_token.access_token}"},
    ) as client:
        yield client
