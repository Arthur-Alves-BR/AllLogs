import pytest

from fastapi import status

from app.models.company import Company


@pytest.mark.asyncio
async def test_get_company(api_client, test_company):
    response = await api_client.get(f"/companies/{test_company.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(test_company.id)


@pytest.mark.asyncio
async def test_get_companies(api_client):
    response = await api_client.get("/companies/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_create_company(api_client):
    data = {"name": "New Company"}
    response = await api_client.post("/companies/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert await Company.exists(id=response.json()["id"])


@pytest.mark.asyncio
async def test_create_company_invalid_data(api_client):
    data = {"name": ""}
    response = await api_client.post("/companies/", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_company(api_client, test_company):
    update_data = {"name": "Updated Company Name"}
    response = await api_client.put(f"/companies/{test_company.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data["id"] == str(test_company.id)
    assert response_data["name"] == update_data["name"]


@pytest.mark.asyncio
async def test_delete_company(api_client, test_company: Company):
    response = await api_client.delete(f"/companies/{test_company.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    await test_company.refresh_from_db()

    assert not test_company.is_active
    assert test_company.deleted_at
