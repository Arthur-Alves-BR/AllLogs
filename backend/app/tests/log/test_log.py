import uuid

from fastapi import status

from app.models.log import Log
from app.core.enums import LogLevel


base_endpoint = "/logs"


async def test_get_log(api_client, test_log):
    response = await api_client.get(f"{base_endpoint}/{test_log.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(test_log.id)


async def test_get_logs(api_client):
    response = await api_client.get(base_endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_create_log(api_client):
    data = {"level": LogLevel.DEBUG, "message": "Test log", "source": str(uuid.uuid4())}
    response = await api_client.post(base_endpoint, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert await Log.get(response.json()["id"])
