import pytest

from fastapi import status


@pytest.mark.asyncio
async def test_get_user(api_client, test_user):
    response = await api_client.get(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(test_user.id)


@pytest.mark.asyncio
async def test_get_users(api_client):
    response = await api_client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
