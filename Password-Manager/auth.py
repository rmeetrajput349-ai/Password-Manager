import bcrypt
from models import get_db

def signup(username, password):
    db = get_db()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, hashed))
        db.commit()
        return True
    except:
        return False

def login(username, password):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

    if user and bcrypt.checkpw(password.encode(), user[2]):
        return user
    return None