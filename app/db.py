import psycopg2
from contextlib import contextmanager

DB_CONFIG = {
    "host":"localhost",
    "port":"5432",
    "user":"hans",
    "password":"860929",
    "dbname":"todo_db"
}

@contextmanager
def get_db():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()