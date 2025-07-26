# Todo API — FastAPI + PostgreSQL 待辦事項專案

## 專案簡介

這是一個以 **FastAPI** 為主體、**PostgreSQL** 為資料庫後端、**Docker** 部署的 RESTful API 專案，實作了基本用戶註冊、登入、JWT 認證、Todo CRUD、自動化測試等功能。  
專案同時搭配 pytest 做 API 自動化測試，並能使用 Docker 打包與快速還原環境，適合學習現代後端開發與作品集展示。

---

## 功能特色

- 用戶註冊、登入、密碼雜湊加密
- JWT Token 認證保護 API
- Todo 清單的 新增/查詢/編輯/刪除（CRUD）
- 自動化 API 測試（pytest）
- 支援 Docker 化部署
- Swagger 自動文件（/docs）

---

## 技術棧

- **Python 3.11+**
- **FastAPI** — 主體 Web 框架
- **PostgreSQL** — 關聯式資料庫
- **psycopg2-binary** — 資料庫連線驅動
- **bcrypt** — 密碼加密
- **python-jose** — JWT 產生與驗證
- **pytest** — 自動化測試
- **Docker** — 部署與交付

---

## 專案結構

```

.
├── app/
│   ├── main.py            # FastAPI 主入口
│   ├── models.py          # Pydantic 輸入/輸出模型
│   ├── db.py              # DB 連線與初始化
│   ├── routes/            # API 路由（auth, todos）
│   ├── services/          # 密碼處理等服務
│   └── utils/             # JWT、token 工具
├── tests/                 # pytest 自動化測試
├── requirements.txt
├── Dockerfile
├── README.md

```

---

## 快速開始

### 1. 環境準備

- 安裝 Python 3.11+ 與 [Docker](https://docs.docker.com/get-docker/)
- 下載/複製本 repo

### 2. 啟動 PostgreSQL 資料庫（用 Docker）

```bash
docker run -d --name todo_postgres \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_PASSWORD=todo_pass \
  -e POSTGRES_DB=todo_db \
  -p 5432:5432 \
  postgres:16
```

### 3. 建立 Python 虛擬環境並安裝依賴

```bash
python -m venv venv
.\venv\Scripts\activate           # Windows
# 或 source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

### 4. 初始化資料表

```bash
python app/init_db.py
```

### 5. 啟動 FastAPI 伺服器

```bash
uvicorn app.main:app --reload
```

* 預設網址：[http://localhost:8000/docs](http://localhost:8000/docs)

---

## API 文件

* **Swagger UI**：[http://localhost:8000/docs](http://localhost:8000/docs)
* 包含：註冊、登入、JWT 權限驗證、Todo CRUD

---

## 自動化測試

```bash
pytest
```

* 所有自動化測試皆在 `tests/` 目錄下

---

## Docker 一鍵部署

### 打包 Image

```bash
docker build -t yourusername/todo-api:latest .
```

### 啟動容器

```bash
docker run -d -p 8000:8000 --env-file .env yourusername/todo-api:latest
```

> **.env** 建議存放 DB 密碼等敏感設定

---

## 重要補充

* **.gitignore** 已排除 venv, **pycache**, .db, .log 等檔案
* 若要本地測試 SQLite，請調整 `db.py` 連線設定
* PostgreSQL 參數可在 Docker run 時自定義

---