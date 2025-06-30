def test_register_login(client):
    # 註冊
    username = "authuser"
    password = "authpass123"
    r = client.post("/api/register", json={"username": username, "password": password})
    assert r.status_code == 200 or r.status_code == 400

    # 登入
    r2 = client.post("/api/login", data={"username": username, "password": password})
    assert r2.status_code == 200
    data = r2.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # 查自己身份
    token = data["access_token"]
    r3 = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert r3.status_code == 200
    assert "msg" in r3.json()


def test_invalid_login(client):
    # 帳號錯誤或密碼錯誤
    r = client.post("/api/login", data={"username": "wrong", "password": "wrong"})
    assert r.status_code == 401