import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from users_manager.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_organization(mock_request):
    mock_request({"id": "1", "name": "FirstOrganization", "status": "created"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "GET",
            "/organization",
            json={"name": "FirstOrganization", "display_name": "GoodSaloon"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "name": "FirstOrganization",
        "status": "created",
    }


@pytest.mark.asyncio
async def test_create_organization_unauthorized():
    response = client.post(
        "organization", json={"name": "FirstOrganization", "display_name": "GoodSaloon"}
    )

    assert response.status_code == 401
    assert "Unauthorized" in response.text
