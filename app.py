
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "finance.db"

# DB初期化
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS income_expense (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        category TEXT,
                        amount INTEGER
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS investments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        stock_name TEXT,
                        price INTEGER
                    )''')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/income")
def income():
    return render_template("income.html")

@app.route("/investment")
def investment():
    return render_template("investment.html")

@app.route("/stock")
def stock():
    return render_template("stock.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = int(request.form["amount"])
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO income_expense (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
        return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/delete", methods=["POST"])
def delete():
    id_to_delete = request.form.get("id")
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM income_expense WHERE id = ?", (id_to_delete,))
    return redirect(url_for("register"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
