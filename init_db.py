import sqlite3

def init_db():
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            status TEXT DEFAULT 'todo'
        )
    ''')
    conn.commit()
    conn.close()
    print("資料表建立完成！")

if __name__ == "__main__":
    init_db()