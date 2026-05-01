import sqlite3
import os

def get_db():
    if not os.path.exists("instance"):
        os.makedirs("instance")
    return sqlite3.connect("instance/database.db")

def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        site TEXT,
        username TEXT,
        password TEXT
    )
    """)

    db.commit()