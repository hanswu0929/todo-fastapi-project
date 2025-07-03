def test_todo_crud(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # 建立 todo
    data = {"title": "測試任務", "content": "pytest測試", "status": "todo", "priority": "medium"}
    r = client.post("/api/todos/", json=data, headers=headers)
    assert r.status_code == 200
    todo_id = r.json()["id"]

    # 查詢全部
    r = client.get("/api/todos/", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert any(todo["id"] == todo_id for todo in r.json())

    # 查詢單一
    r = client.get(f"/api/todos/{todo_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["title"] == "測試任務"

    # 修改
    update_data = {"title": "修改任務", "content": "已完成", "status": "done", "priority": "medium"}
    r = client.put(f"/api/todos/{todo_id}", json=update_data, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "done"

    # 刪除
    r = client.delete(f"/api/todos/{todo_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"] == "刪除成功"

def test_todo_unauthorized(client):
    # 沒帶 token 就 CRUD
    r = client.get("/api/todos/")
    assert r.status_code == 401

def test_get_nonexist_todo(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # 查詢一個不存在的 id
    r = client.get("/api/todos/999999", headers=headers)
    assert r.status_code == 404
    assert r.json()["detail"] == "找不到該待辦事項"

def test_update_nonexit_todo(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"title": "測試標題", "content": "測試內容", "status": "done", "priority": "low"}
    r = client.put("/api/todos/999999", json=data, headers=headers)
    assert r.status_code == 404
    assert r.json()["detail"] == "找不到該待辦事項"