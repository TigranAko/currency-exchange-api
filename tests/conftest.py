import httpx
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.base import BaseModel
from app.models.user import User
from app.services.external_api_service import ExternalAPIService
from main import app

print(User)

url = "sqlite:///:memory:"
engine = create_engine(
    url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
Session = sessionmaker(engine, autoflush=False)
BaseModel.metadata.create_all(engine)


# @pytest.fixture(scope="function")
def session_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


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
        "data": {"username": "test"},
    }
    response = client.post("/auth/login", params=user)
    assert response.status_code == 200
    cookies = response.cookies
    assert "access_token_cookie" in cookies
    assert "csrf_access_token" in cookies


@pytest_asyncio.fixture
async def mock_httpx_client():
    """Фикстура для мок-клиента"""
    async with httpx.AsyncClient() as client:
        yield client


@pytest.fixture
def api_service(mock_httpx_client):
    """Фикстура для сервиса"""
    headers = {"apikey": "secret_api_key"}
    return ExternalAPIService(mock_httpx_client, headers=headers)
