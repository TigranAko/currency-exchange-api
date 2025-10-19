from fastapi.testclient import TestClient
from main import app

import pytest


client = TestClient(app)


def test_register():
    response = client.post("/auth/register", json={"username": "user", "password": "pass"})
    assert response.status_code == 200
    data = response.json()
    assert data == "Вы зарегестрированы"


def test_login():
    login_data = {"username": "test", "password": "password"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    cookies = response.cookies
    assert "access_token_cookie" in cookies
    assert "csrf_access_token" in cookies


@pytest.mark.parametrize(
        "creds",
        [
            {},
            {"usenmae": "username"},
            {"password": "pass"}
        ]
)
def test_register_errors(creds):
    response = client.post("/auth/register", json=creds)
    assert response.status_code == 422


@pytest.mark.parametrize(
        "creds, status_code",
        [
            [{}, 422],
            [{"usenmae": "username"}, 422],
            [{"password": "pass"}, 422],
            [{"username": "no_username", "password": "password"}, 401],
            [{"username": "test", "password": "no_password"}, 401],
            [{"username": "no_username", "password": "no_password"}, 401]
        ]
)
def test_login_errors(creds, status_code):
    response = client.post("/auth/login", json=creds)
    assert response.status_code == status_code
    cookies = response.cookies
    assert "access_token_cookie" not in cookies
    assert "csrf_access_token" not in cookies


def test_register_and_login():
    user = {"username": "user", "password": "pass"}
    response = client.post("/auth/register", json=user)
    assert response.status_code == 200
    data = response.json()
    assert data == "Вы зарегестрированы"

    response = client.post("/auth/login", json=user)
    assert response.status_code == 200
    cookies = response.cookies
    assert "access_token_cookie" in cookies
    assert "csrf_access_token" in cookies

