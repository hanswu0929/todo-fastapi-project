from app.db import get_db

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(20) UNIQUE NOT NULL,
                password VARCHAR(128) NOT NULL
            ) 
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title VARCHAR(30) NOT NULL,
                content VARCHAR(200) NOT NULL,
                status VARCHAR(10) DEFAULT 'todo',
                owner VARCHAR(20) NOT NULL,
                priority VARCHAR(10) NOT NULL
            )
        ''')

        conn.commit()

    print("PostgreSQL 資料表建立完成！")

if __name__ == "__main__":
    init_db()