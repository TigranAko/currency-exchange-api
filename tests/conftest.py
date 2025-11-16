import pytest

from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def protected(client):
    user = {"username": "test", "password": "test"}
    response = client.post("/auth/register", params=user)
    assert response.status_code == 200
    data = response.json()
    assert data == {
            "ok": True,
            "message": "Вы зарегестрированы",
            "data": {
                "username": "test"
                }
            }
    response = client.post("/auth/login", params=user)
    assert response.status_code == 200
    cookies = response.cookies
    assert "access_token_cookie" in cookies
    assert "csrf_access_token" in cookies

