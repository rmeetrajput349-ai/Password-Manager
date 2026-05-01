from flask import Flask, render_template, request, redirect, session
import sqlite3, hashlib

app = Flask(__name__)
app.secret_key = "secret123"

# Database setup
def get_db():
    return sqlite3.connect("instance/database.db")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = hashlib.sha256(request.form['password'].encode()).hexdigest()

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        data = cur.fetchone()

        if data:
            session['user'] = user
            return redirect('/dashboard')
        else:
            return render_template("login.html", error="Invalid ID or Password")

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = hashlib.sha256(request.form['password'].encode()).hexdigest()

        db = get_db()
        cur = db.cursor()

        # check existing
        cur.execute("SELECT * FROM users WHERE username=?", (user,))
        if cur.fetchone():
            return render_template('register.html', error="This ID already exists")

        # insert
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
        db.commit()

        return redirect('/')

    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/')
    db = get_db()
    if request.method == 'POST':
        site = request.form['site']
        username= request.form['username']
        password = request.form['password']
        db.execute("INSERT INTO passwords (user, site, username, password) VALUES (?, ?, ?, ?)", (session['user'], site, request.form['username'], password))
        db.commit()
    data = db.execute("SELECT id, site, username, password FROM passwords WHERE user=?", (session['user'],))
    return render_template('dashboard.html', data=data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

from flask import redirect

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()   # ya jo tum use kar rahe ho
    db.execute("DELETE FROM passwords WHERE id = ?", (id,))
    db.commit()
    return redirect("/dashboard")

def init_db():
    import sqlite3
    db = sqlite3.connect("instance/database.db")  # IMPORTANT: same path
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

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
if __name__ == "__main__":
    init_db()
    app.run(debug=True)