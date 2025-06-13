````markdown
# 待辦事項 FastAPI Project

## 專案簡介
本專案為一個使用 FastAPI + SQLite 開發的待辦事項管理 API，支援註冊、登入、JWT 權限驗證，以及完整 CRUD 操作。

## 安裝與啟動

```bash
git clone https://github.com/你的帳號/你的repo.git
cd 專案資料夾
pip install -r requirements.txt
uvicorn main:app --reload
````

## API 規格與文件

* **/register**：用戶註冊
* **/login**：用戶登入，取得 JWT Token
* **/todos**：CRUD 操作（需帶入 JWT Token）
* 進一步的 API 規格，可於啟動後至 `/docs`（Swagger UI）查看

## 測試方式

1. 啟動伺服器後，開啟 [http://localhost:8000/docs](http://localhost:8000/docs)
2. 直接於 Swagger UI 測試所有 API 功能
3. 建議先註冊 → 登入取得 JWT → 測試 todos CRUD

## 主要技術與套件

* FastAPI
* Pydantic
* SQLite
* Bcrypt
* PyJWT

## 目錄結構

```
app/
  main.py
  models.py
  db.py
  routes/
    auth.py
    todos.py
  services/
    auth_services.py
  utils/
    auth_tool.py
    jwt_tools.py
  requirements.txt
  README.md
  init_db.py
  .gitignore
```