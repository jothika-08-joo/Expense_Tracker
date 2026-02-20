import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
#from datatime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24).hex())


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn
'''
def create_users_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            budget REAL DEFAULT 0,
            
        )
    """)
    conn.commit()
    conn.close()
'''

def check_table():
    conn = get_db_connection()
    

def create_expenses_table():
    conn = get_db_connection()
    # Drop old table
    conn.execute("DROP TABLE IF EXISTS expenses;")
    
    # Create new table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]    
    if request.method == "POST":
        title = request.form["title"]
        amount = float(request.form["amount"])
        category=request.form["category"]
        
        date = request.form["date"]

        conn= get_db_connection()
        conn.execute(
            "INSERT INTO expenses (title, amount,category, date, user_id) VALUES(?, ?, ?, ?)",
            (title, amount, date, session["user_id"])
        )
        conn.commit()
        conn.close()
        return redirect("/user")
    return render_template("add_expense.html")    

'''
@app.route("/insert")
def insert():
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users ( name, email, password, role) VALUES (?, ?, ?, ?)",
        ("admin", "admin@gmail.com", "admin123", "admin")

    )
    conn.execute(
        "INSERT INTO users ( name, email, password, role) VALUES (?, ?, ?, ?)",
        ("jothika", "jothika@gmail.com", "user123", "user")
        
    )
    
    conn.commit()
    conn.close()
    return "added"
'''

'''
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("""
    SELECT * FROM users
    """).fetchall()
    conn.close()
    return users
'''
@app.route("/")
def home():
    
    return render_template("home.html")  
    


 

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        

        conn = get_db_connection()
       
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES(?, ?, ?, ?)",
            (name, email, hashed_password, "user")
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")
    return render_template("login.html")     

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"] 

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)

        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"],password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/dashboard")
        return "Invalid credentials"            
    return render_template("login.html") 

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    if session["role"] == "admin":
        return redirect("/admin")
    return redirect("/user")    

   

@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session or session["role"] !="admin":
        return redirect("/login")
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
        
    conn.close()
    return render_template("admin_dashboard.html", users=users, expenses=expenses)


@app.route("/user")
def user_dashboard():
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    conn = get_db_connection()
    expenses = conn.execute(
        "SELECT * FROM expenses WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    total = conn.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id = ?",
        (user_id,)
    ).fetchone()[0] or 0

    category_totals = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "user_dashboard.html",
        expenses=expenses,
        total=total,
        category_totals=category_totals
    )


    month = "2026-01" #later UI
    monthly_total = conn.execute(
        """ 
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id = ?
        AND strftime('%Y-%m', date) = ?
        """,
        (user_id, month)

    ).fetchone()[0] or 0

    year = "2026"
    yearly_total = conn.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id  = ?
        AND strftime('%Y', date) = ?
        """,
        (user_id, year)
    ).fetchone()[0] or 0

    row = conn.execute(
        "SELECT budget FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    budget = row ["budget"] if row ["budget"] is not None else 0
    

    conn.close()

    

    return render_template(
        "user_dashboard.html",
        expenses=expenses,
        total=total,
        monthly_total=monthly_total,
        yearly_total=yearly_total,
        budget=budget
    )

@app.route("/debug_users")
def debug_users():
    users = get_all_users()

    print("total users:",len(users))

    for user in users:
        print(dict(user))
    return "Check terminal"

if __name__ == "__main__":
    create_expenses_table()
    app.run(debug=True)    

