import uuid

from fastapi import status

from app.models import Application


base_endpoint = "/applications"


async def test_get_application(api_client, test_application):
    response = await api_client.get(f"{base_endpoint}/{test_application.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(test_application.id)


async def test_get_applications(api_client):
    response = await api_client.get(base_endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_create_application(api_client, test_company):
    data = {
        "name": "New App",
        "description": "Test app",
        "company_id": str(test_company.id),
    }
    response = await api_client.post(base_endpoint, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert await Application.exists(id=response.json()["id"])


async def test_create_application_with_invalid_company_id(api_client):
    data = {
        "name": "New App",
        "description": "Test app",
        "company_id": str(uuid.uuid4()),
    }
    response = await api_client.post(base_endpoint, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_update_application(api_client, test_application):
    update_data = {"name": "Updated App Name"}
    response = await api_client.put(f"{base_endpoint}/{test_application.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data["id"] == str(test_application.id)
    assert response_data["name"] == update_data["name"]


async def test_delete_application(api_client, test_application):
    response = await api_client.delete(f"{base_endpoint}/{test_application.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    await test_application.refresh_from_db()

    assert not test_application.is_active
    assert test_application.deleted_at
