import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from users_manager.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_organization(mock_request):
    mock_request({"id": "1", "name": "FirstOrganization"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "GET", "/organization", json={"name": "FirstOrganization"}
        )

    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "FirstOrganization"}


@pytest.mark.asyncio
async def test_get_organization_unauthorized():
    response = client.request(
        "GET", "/organization", json={"name": "FirstOrganization"}
    )

    assert response.status_code == 401
    assert "Unauthorized" in response.text


@pytest.mark.asyncio
async def test_get_organizations(mock_request):
    mock_request(
        [
            {"id": "1", "name": "FirstOrganization"},
            {"id": "2", "name": "SecondOrganization"},
        ]
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "GET", "/organizations", json={"tenant_domain": "test-domain"}
        )

    assert response.status_code == 200
    assert response.json() == [
        {"id": "1", "name": "FirstOrganization"},
        {"id": "2", "name": "SecondOrganization"},
    ]


@pytest.mark.asyncio
async def test_get_organizations_unauthorized():
    response = client.request(
        "GET", "/organizations", json={"tenant_domain": "test-domain"}
    )

    assert response.status_code == 401
    assert "Unauthorized" in response.text
