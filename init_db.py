from app.db import get_db

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        # rollback journal -> Write-Ahead Logging，多個讀取可以跟寫入同時進行
        cursor.execute("PRAGMA journal_mode=WAL;")
        # 建 users 表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # 建 todos 表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                status TEXT DEFAULT 'todo',
                owner TEXT NOT NULL,
                priority TEXT NOT NULL
            )
        ''')
        conn.commit()
    print("資料表建立完成！")

if __name__ == "__main__":
    init_db()