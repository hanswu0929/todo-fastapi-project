from fastapi import APIRouter, HTTPException, status, Form, Depends
import sqlite3
import logging
from app.models import UserCreate, Token
from app.db import get_db
from app.utils.jwt_tools import create_token
from app.services.auth_service import hash_password, verify_password
from app.utils.auth_tool import verify_token

router = APIRouter()


# 註冊 API
@router.post("/register", response_model=dict, summary="註冊新用戶")
def register(user: UserCreate):
    with get_db() as conn:
        hashed_password = hash_password(user.password)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user.username, hashed_password)
            )
            conn.commit()
            logging.info(f"註冊成功: {user.username}")
        except sqlite3.IntegrityError:
            logging.error(f"註冊失敗，帳號已存在: {user.username}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用戶名已存在")
    return {"msg": "註冊成功"}


# 登入 API（用表單格式才能配合 Swagger Oauth2）
@router.post("/login", response_model=Token, summary="用戶登入，取得 JWT Token")
def login(username: str = Form(...), password: str = Form(...)):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE username=?",
                (username,)
            )
            row = cursor.fetchone()
            if not row or not verify_password(password, row[0]):
                logging.warning(f"登入失敗，帳號或密碼錯誤: {username}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="帳號或密碼錯誤")
        token = create_token(username)
        logging.info(f"登入成功: {username}")
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"登入流程發生未預期例外: {str(e)}，帳號: {username}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="伺服器內部錯誤，請稍後再試")
    

# 受保護測試 API
@router.get("/me", summary="查詢自己身分")
def read_me(username: str = Depends(verify_token)):
    return {"msg": f"你目前以 {username} 身分登入"}