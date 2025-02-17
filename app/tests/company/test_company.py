from fastapi import status

from app.models.company import Company


base_endpoint = "/companies"


async def test_get_company(api_client, test_company):
    response = await api_client.get(f"{base_endpoint}/{test_company.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(test_company.id)


async def test_get_companies(api_client):
    response = await api_client.get(base_endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_create_company(api_client):
    data = {"name": "New Company"}
    response = await api_client.post(base_endpoint, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert await Company.exists(id=response.json()["id"])


async def test_create_company_invalid_data(api_client):
    data = {"name": ""}
    response = await api_client.post(base_endpoint, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_update_company(api_client, test_company):
    update_data = {"name": "Updated Company Name"}
    response = await api_client.put(f"{base_endpoint}/{test_company.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data["id"] == str(test_company.id)
    assert response_data["name"] == update_data["name"]


async def test_delete_company(api_client, test_company: Company):
    response = await api_client.delete(f"{base_endpoint}/{test_company.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    await test_company.refresh_from_db()

    assert not test_company.is_active
    assert test_company.deleted_at
