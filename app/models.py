from pydantic import BaseModel, Field, StringConstraints  # 型別限制
from typing import Annotated  # 同時為欄位加型別、格式限制、欄位說明
from enum import Enum  # 列舉型別驗證: 一種「把一個欄位的可選值限制在特定幾個選項之內」的型別


# 狀態列舉型別：只允許 "todo" 與 "done"
class StatusEnum(str, Enum):
    todo = "todo"
    done = "done"


# 建立/修改 ToDo 時的輸入資料結構
class TodoIn(BaseModel):
    title: Annotated[
        str,
        StringConstraints(min_length=2, max_length=30),
            Field(..., description="標題長度需2~30字")
    ]
    content: Annotated[
        str,
        StringConstraints(min_length=1, max_length=200),
        Field(..., description="內容長度需1~200字")
    ]
    status: StatusEnum = Field(StatusEnum.todo, description="狀態:todo 或 done")


# 查詢 ToDo、回傳給前端時
class TodoOut(TodoIn):
    id: int = Field(..., ge=1, description="資料ID，必須大於0")
    owner: str   # 擁有者 username，與 JWT 做結合


# 用戶註冊/登入
class UserCreate(BaseModel):
    username: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=20,
            pattern="^[a-zA-Z0-9_]+$"
        ),
        Field(..., description="只允許英數字與底線")
    ]
    password: Annotated[
        str,
        StringConstraints(min_length=6, max_length=32),
        Field(..., description="密碼需6~32字")
    ]


# 回傳 token 給前端
class Token(BaseModel):
    access_token: str
    token_type: str