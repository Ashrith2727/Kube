from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME"),
    )

@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT message FROM messages;")
    data = cur.fetchall()
    return render_template("index.html", messages=data)

@app.route("/add", methods=["POST"])
def add():
    msg = request.form["message"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages(message) VALUES (%s)", (msg,))
    conn.commit()
    return "<h3>Message added</h3><a href='/'>Go Back</a>"

app.run(host="0.0.0.0", port=5000)
