import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from users_manager.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_modify_organization(mock_request):
    mock_request({"identifier": "1234", "display_name": "NewGoodSaloon"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "PUT",
            "/organization",
            json={"identifier": "1234", "display_name": "NewGoodSaloon"},
        )

    assert response.status_code == 200
    assert response.json() == {"identifier": "1234", "display_name": "NewGoodSaloon"}


@pytest.mark.asyncio
async def test_modify_organization_unauthorized():

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "PUT",
            "/organization",
            json={"identifier": "1234", "display_name": "NewGoodSaloon"},
        )

    assert response.status_code == 401
    assert "Unauthorized" in response.text
