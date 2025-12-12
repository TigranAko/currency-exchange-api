import pytest

from app.dependencies.database import get_session
from main import app

from .conftest import session_db

# client = TestClient(app)


def test_register(client):
    app.dependency_overrides[get_session] = session_db
    response = client.post(
        "/auth/register", params={"username": "user", "password": "pass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    app.dependency_overrides = {}


def test_login(client):
    app.dependency_overrides[get_session] = session_db
    user = {"username": "test", "password": "password"}
    response = client.post("/auth/register", params=user)
    assert response.status_code == 200  # 201

    response = client.post("/auth/login", params=user)
    assert response.status_code == 200
    cookies = response.cookies
    assert "access_token_cookie" in cookies
    assert "csrf_access_token" in cookies
    app.dependency_overrides = {}


@pytest.mark.parametrize("creds", [{}, {"usenmae": "username"}, {"password": "pass"}])
def test_register_errors(client, creds):
    response = client.post("/auth/register", params=creds)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "creds, status_code",
    [
        [{}, 422],
        [{"usenmae": "username"}, 422],
        [{"password": "pass"}, 422],
        [{"username": "no_username", "password": "password"}, 401],
        [{"username": "test", "password": "no_password"}, 401],
        [{"username": "no_username", "password": "no_password"}, 401],
    ],
)
def test_login_errors(client, creds, status_code):
    response = client.post("/auth/login", params=creds)
    assert response.status_code == status_code
    cookies = response.cookies
    assert "access_token_cookie" not in cookies
    assert "csrf_access_token" not in cookies
