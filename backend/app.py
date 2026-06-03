from flask import Flask
from data import get_connection
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is working!"

@app.route('/test-db')
def test_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1;")
    result = cur.fetchone()

    cur.close()
    conn.close()

    return f"DB Connected: {result}"

@app.route('/add-user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )

    conn.commit()
    cur.close()
    conn.close()

    return "User added successfully"


if __name__ == '__main__':
    app.run(debug=True)