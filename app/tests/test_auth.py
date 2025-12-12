import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ...core.config import settings
from ...main import app
from ...models.schemas import User

client = TestClient(app)

def test_login_success():
    """Test successful login."""
    # This is a mock test - in a real app, you would use a test database
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "nonexistent", "password": "wrongpassword"},
    )
    assert response.status_code == 401

def test_read_users_me(
    test_user: User, test_token: str, client: TestClient
) -> None:
    """Test reading the current user."""
    response = client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == test_user.email

# Fixtures for testing
@pytest.fixture
def test_user() -> User:
    """Create a test user."""
    return User(
        id=1,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True,
    )

@pytest.fixture
def test_token(test_user: User) -> str:
    """Create a test token."""
    from ...services.auth_service import auth_service
    return auth_service.create_access_token(
        data={"sub": test_user.email},
        expires_delta=None,
    )
