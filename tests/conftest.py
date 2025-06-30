import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture
def user_token(client):
    # 建立新帳號並登入取得 token（帳號重複時自動跳過註冊）
    username = "pytestuser"
    password = "pytestpass123"
    client.post("/api/register", json={"username": username, "password": password})
    resp = client.post("/api/login", data={"username": username, "password": password})
    return resp.json()["access_token"]