from pydantic import BaseModel, Field
from enum import Enum  # 列舉型別驗證: 一種「把一個欄位的可選值限制在特定幾個選項之內」的型別

class StatusEnum(str, Enum):
    todo = "todo"
    done = "done"

class Todo(BaseModel):
    title: str = Field(..., min_length=2, max_length=30, description="標題長度需2~30字")
    content: str = Field(..., min_length=1, max_length=200, description="內容長度需1~200字")
    status: StatusEnum = Field(StatusEnum.todo, description="狀態:todo 或 done")