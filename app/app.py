from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.getenv("DB_PATH", "tasks.db")


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due TEXT NOT NULL,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def check_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except:
        return False


@app.route("/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    priority = request.args.get("priority")

    conn = connect_db()

    if status and priority:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE status = ? AND priority = ?",
            (status, priority)
        ).fetchall()
    elif status:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE status = ?",
            (status,)
        ).fetchall()
    elif priority:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE priority = ?",
            (priority,)
        ).fetchall()
    else:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()

    conn.close()

    result = []
    for task in tasks:
        result.append(dict(task))

    return jsonify(result)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON"}), 400

    title = data.get("title")
    due = data.get("due")
    priority = data.get("priority")

    if not title or not due or priority is None:
        return jsonify({"error": "title, due and priority are required"}), 400

    if not check_date(due):
        return jsonify({"error": "Wrong date format"}), 400

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (title, due, priority, status) VALUES (?, ?, ?, ?)",
        (title, due, priority, "open")
    )

    task_id = cur.lastrowid
    conn.commit()

    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    return jsonify(dict(task)), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON"}), 400

    status = data.get("status")

    if not status:
        return jsonify({"error": "status is required"}), 400

    conn = connect_db()

    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()

    updated_task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    return jsonify(dict(updated_task))


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = connect_db()

    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
