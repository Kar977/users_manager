import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from users_manager.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_delete_user_from_organization(mock_request):
    mock_request({"user_id": "1", "organization_id": "10"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "DELETE",
            "/organization/user",
            json={"user_id": "1", "organization_id": "10"},
        )

    assert response.status_code == 201
    assert response.json() == {"user_id": "1", "organization_id": "10"}


@pytest.mark.asyncio
async def test_delete_not_existing_user_from_not_existing_organization():

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "DELETE",
            "/organization/user",
            json={"user_id": "1", "organization_id": "10"},
        )

    assert response.status_code == 404
    assert "Not Found" in response.text
