import pytest

from fastapi import status


@pytest.mark.asyncio
async def test_health_check(api_client) -> None:
    response = await api_client.get("/health_check")
    assert response.status_code == status.HTTP_200_OK
