import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect("todos.db", timeout=10) # 加長等待時間
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()