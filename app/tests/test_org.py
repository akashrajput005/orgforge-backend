import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ...core.config import settings
from ...main import app
from ...models.schemas import Organization, UserOrganization

client = TestClient(app)

def test_create_organization(test_token: str):
    """Test creating an organization."""
    org_data = {
        "name": "Test Org",
        "description": "A test organization"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/orgs/",
        json=org_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == org_data["name"]
    assert data["description"] == org_data["description"]
    assert "id" in data

def test_list_organizations(test_token: str):
    """Test listing organizations."""
    response = client.get(
        f"{settings.API_V1_STR}/orgs/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # If there are organizations
        assert "id" in data[0]
        assert "name" in data[0]

def test_get_organization(test_token: str, test_org: Organization):
    """Test getting a single organization."""
    response = client.get(
        f"{settings.API_V1_STR}/orgs/{test_org.id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_org.id
    assert data["name"] == test_org.name

# Fixtures for testing
@pytest.fixture
def test_org() -> Organization:
    """Create a test organization."""
    return Organization(
        id=1,
        name="Test Org",
        description="A test organization",
        is_active=True,
    )

@pytest.fixture
def test_user_org(test_org: Organization, test_user) -> UserOrganization:
    """Create a test user organization relationship."""
    return UserOrganization(
        id=1,
        user_id=test_user.id,
        organization_id=test_org.id,
        role="admin",
        is_active=True,
    )
