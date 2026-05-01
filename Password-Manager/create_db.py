import sqlite3

db = sqlite3.connect("instance/database.db")
cur = db.cursor()

# users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# passwords table
cur.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    site TEXT,
    username TEXT,
    password TEXT
)
""")

db.commit()
db.close()

print("Database & tables created successfully")