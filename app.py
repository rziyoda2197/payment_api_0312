from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        balance INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        receiver_id INTEGER,
        amount INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO users (name, balance) VALUES (?, ?)",
        (data["name"], data.get("balance", 0)),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User created"})


@app.route("/users", methods=["GET"])
def list_users():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users = c.fetchall()

    conn.close()

    return jsonify(users)


@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.json

    sender = data["sender_id"]
    receiver = data["receiver_id"]
    amount = data["amount"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT balance FROM users WHERE id=?", (sender,))
    sender_balance = c.fetchone()

    if not sender_balance:
        return jsonify({"error": "Sender not found"}), 404

    if sender_balance[0] < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    c.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, sender))
    c.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, receiver))

    c.execute(
        """
        INSERT INTO transactions (sender_id, receiver_id, amount, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (sender, receiver, amount, datetime.datetime.utcnow().isoformat()),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Transfer successful"})


@app.route("/transactions", methods=["GET"])
def transactions():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM transactions")
    rows = c.fetchall()

    conn.close()

    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
