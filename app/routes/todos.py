from fastapi import APIRouter, HTTPException, Depends, status
from app.models import TodoIn, TodoOut
from app.db import get_db
from app.utils.auth_tool import verify_token
import logging

router = APIRouter()

# Create
@router.post("/todos/", response_model=TodoOut)
# 強制 API 回傳資料格式符合定義的 Pydantic 模型
# 送出的資料格式錯誤、缺欄位、型別不符（例如 title 太短、status 不是 todo/done），
# 這時候錯誤發生在進入 route function 之前，也就是「進到 create_todo 函式之前」就被 FastAPI + Pydantic 攔下來了
# 所以 try/except 和 logging.error 根本沒有被執行到

def create_todo(todo: TodoIn, username: str = Depends(verify_token)):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO todos (title, content, status, owner, priority) VALUES (?, ?, ?, ?, ?)",
                (todo.title, todo.content, todo.status, username, todo.priority)
            )
            conn.commit()
            todo_id = cursor.lastrowid
            return TodoOut.model_validate({"id": todo_id, "owner": username, **todo.model_dump()})
    except Exception as e:
        logging.error(f"資料寫入失敗 {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="資料寫入失敗，請聯絡管理員")


# Read All
@router.get("/todos/", response_model=list[TodoOut])
def get_todos(username: str = Depends(verify_token)):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos WHERE owner=?", (username,))
            rows = cursor.fetchall()
            return [TodoOut.model_validate(dict(row)) for row in rows]
    except Exception as e:
        logging.error(f"查詢全部資料失敗 {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="查詢資料失敗，請聯絡管理員")


# Read One
@router.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, username: str = Depends(verify_token)):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos WHERE id=? AND owner=?", (todo_id, username))
            row = cursor.fetchone()
            if row:
                return TodoOut.model_validate(dict(row))
                # .model_validate()永遠只接受一個 dict 當作參數
                # Pydantic 2.x 新增的方法：允許你直接把任意資料型態（如 dict 或物件）轉換成 Pydantic Model 實例
                # 功能類似舊版的 parse_obj()，但命名更清楚，設計更直觀
                # 它會自動幫你過濾、校驗欄位，甚至支援巢狀物件與型別自動轉換
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到該待辦事項")
    except Exception as e:
        logging.error(f"查詢單筆資料失敗 {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="查詢資料失敗，請聯絡管理員")


# Update
@router.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, todo: TodoIn, username: str = Depends(verify_token)):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE todos SET title=?, content=?, status=? , priority=? WHERE id=? AND owner=?",
                (todo.title, todo.content, todo.status, todo.priority, todo_id, username)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到該待辦事項")
            return TodoOut.model_validate({"id": todo_id, "owner": username, **todo.model_dump()})
    except Exception as e:
        logging.error(f"資料更新失敗 {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新資料失敗，請聯絡管理員")


# Delete
@router.delete("/todos/{todo_id}") # 回傳值簡單，不需response_model
def delete_todo(todo_id: int, username: str = Depends(verify_token)):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE id=? AND owner=?", (todo_id, username))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到該待辦事項")
            return {"message": "刪除成功", "id": todo_id}
    except Exception as e:
        logging.error(f"刪除資料失敗 {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="刪除資料失敗，請聯絡管理員")