from fastapi import APIRouter, HTTPException
from app.models import Todo
from app.db import get_db
import logging

router = APIRouter()

# Create
@router.post("/todos/", response_model=Todo)
# 強制 API 回傳資料格式符合定義的 Pydantic 模型
# 送出的資料格式錯誤、缺欄位、型別不符（例如 title 太短、status 不是 todo/done），
# 這時候錯誤發生在進入 route function 之前，也就是「進到 create_todo 函式之前」就被 FastAPI + Pydantic 攔下來了
# 所以 try/except 和 logging.error 根本沒有被執行到

def create_todo(todo: Todo):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, content, status) VALUES (?, ?, ?)",
            (todo.title, todo.content, todo.status)
        )
        conn.commit()
        conn.close()
        return todo
    except Exception as e:
        logging.error(f"資料寫入失敗 {str(e)}")
        raise HTTPException(status_code=500, detail="資料寫入失敗，請聯絡管理員")

# Read All
@router.get("/todos/", response_model=list[Todo])
def get_todos():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        conn.close()
        return [Todo(**dict(row)) for row in rows]
        # 參數拆包（dictionary unpacking）語法 
        # 自動把 dict 內的每個 key 對應到 Todo model 的欄位名稱
    except Exception as e:
        logging.error(f"查詢全部資料失敗 {str(e)}")
        raise HTTPException(status_code=500, detail="查詢資料失敗，請聯絡管理員")

# Read One
@router.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id=?", (todo_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Todo(**dict(row))
        raise HTTPException(status_code=404, detail="找不到該待辦事項")
    except Exception as e:
        logging.error(f"查詢單筆資料失敗 {str(e)}")
        raise HTTPException(status_code=500, detail="查詢資料失敗，請聯絡管理員")

# Update
@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET title=?, content=?, status=? WHERE id=?",
            (todo.title, todo.content, todo.status, todo_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="找不到該待辦事項")
        conn.close()
        return todo
    except Exception as e:
        logging.error(f"資料更新失敗 {str(e)}")
        raise HTTPException(status_code=500, detail="更新資料失敗，請聯絡管理員")

# Delete
@router.delete("/todos/{todo_id}") # 回傳值簡單，不需response_model
def delete_todo(todo_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id=?", (todo_id,))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="找不到該待辦事項")
        conn.close()
        return {"message": "刪除成功", "id": todo_id}
    except Exception as e:
        logging.error(f"刪除資料失敗 {str(e)}")
        raise HTTPException(status_code=500, detail="刪除資料失敗，請聯絡管理員")