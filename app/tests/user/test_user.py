import uuid

from fastapi import status

from app.models import User


base_endpoint = "/users"


async def test_get_user(api_client, test_user):
    response = await api_client.get(f"{base_endpoint}/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(test_user.id)


async def test_get_users(api_client):
    response = await api_client.get(base_endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_create_user(api_client, test_company):
    data = {
        "name": "New User",
        "password": "Ag$234gsrgh",
        "email": "test@gmail.com",
        "company_id": str(test_company.id),
    }
    response = await api_client.post(base_endpoint, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert await User.exists(id=response.json()["id"])


async def test_create_user_with_invalid_company_id(api_client):
    data = {
        "name": "New User 2",
        "password": "Ag$234gsrgh",
        "email": "test@gmail.com",
        "company_id": str(uuid.uuid4()),
    }
    response = await api_client.post(base_endpoint, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_update_user(api_client, test_user):
    update_data = {"name": "Updated User Name"}
    response = await api_client.put(f"{base_endpoint}/{test_user.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data["id"] == str(test_user.id)
    assert response_data["name"] == update_data["name"]


async def test_delete_user(api_client, test_user):
    response = await api_client.delete(f"{base_endpoint}/{test_user.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    await test_user.refresh_from_db()

    assert not test_user.is_active
    assert test_user.deleted_at
