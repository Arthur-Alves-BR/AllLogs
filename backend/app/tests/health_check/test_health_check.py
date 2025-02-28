from fastapi import status


async def test_health_check(api_client) -> None:
    response = await api_client.get("/health_check")
    assert response.status_code == status.HTTP_200_OK
