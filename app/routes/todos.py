from fastapi import APIRouter, HTTPException
from app.models import Todo
from app.db import get_db

router = APIRouter()

# Create
@router.post("/todos/", response_model=Todo)  # 強制 API 回傳資料格式符合定義的 Pydantic 模型
def create_todo(todo: Todo):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (title, content, status) VALUES (?, ?, ?)",
        (todo.title, todo.content, todo.status)
    )
    conn.commit()
    conn.close()
    return todo

# Read All
@router.get("/todos/")
def get_todos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM toods")
    rows = cursor.fetchall()
    conn.close()
    return [Todo(**dict(row)) for row in rows]
    # 參數拆包（dictionary unpacking）語法 
    # 自動把 dict 內的每個 key 對應到 Todo model 的欄位名稱

# Read One
@router.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE id=?", (todo_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Todo(**dict(row))
    raise HTTPException(status_code=404, detail="找不到該待辦事項")

# Update
@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todos SET title=?, content=?, status=? WHERE id=?",
        (todo.title, todo.content, todo.status, todo_id)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到該待辦事項")
    conn.close()
    return todo

# Delete
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到該待辦事項")
    conn.close()
    return {"message": "刪除成功", "id": todo_id}