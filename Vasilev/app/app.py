import os
import random
import sqlite3
from contextlib import closing

from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "jokes.db")


def connect_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)

    with closing(connect_db()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                category TEXT NOT NULL,
                votes INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


def to_json(row):
    return {
        "id": row["id"],
        "text": row["text"],
        "category": row["category"],
        "votes": row["votes"],
    }


def error(message, code):
    return jsonify({"error": message}), code


def load_jokes(category=None):
    with closing(connect_db()) as conn:
        if category:
            rows = conn.execute(
                "SELECT id, text, category, votes FROM jokes WHERE category = ? ORDER BY id",
                (category,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, text, category, votes FROM jokes ORDER BY id"
            ).fetchall()

        return [to_json(row) for row in rows]


def load_random_joke(category=None):
    jokes = load_jokes(category)
    if not jokes:
        return None
    return random.choice(jokes)


def save_joke(text, category):
    with closing(connect_db()) as conn:
        cur = conn.execute(
            "INSERT INTO jokes (text, category) VALUES (?, ?)",
            (text, category),
        )
        conn.commit()

        row = conn.execute(
            "SELECT id, text, category, votes FROM jokes WHERE id = ?",
            (cur.lastrowid,),
        ).fetchone()

        return to_json(row)


def vote_joke(joke_id, vote_value):
    delta = 1 if vote_value == "up" else -1

    with closing(connect_db()) as conn:
        found = conn.execute(
            "SELECT id FROM jokes WHERE id = ?",
            (joke_id,),
        ).fetchone()

        if found is None:
            return None

        conn.execute(
            "UPDATE jokes SET votes = votes + ? WHERE id = ?",
            (delta, joke_id),
        )
        conn.commit()

        row = conn.execute(
            "SELECT id, text, category, votes FROM jokes WHERE id = ?",
            (joke_id,),
        ).fetchone()

        return to_json(row)


@app.route("/jokes", methods=["GET"])
def get_jokes():
    category = request.args.get("category", type=str)
    return jsonify(load_jokes(category)), 200


@app.route("/jokes/random", methods=["GET"])
def get_random_joke():
    category = request.args.get("category", type=str)
    joke = load_random_joke(category)

    if joke is None:
        return error("No jokes found", 404)

    return jsonify(joke), 200


@app.route("/jokes", methods=["POST"])
def add_joke():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()
    category = str(payload.get("category", "")).strip()

    if not text or not category:
        return error("Missing text or category", 400)

    created = save_joke(text, category)
    return jsonify(created), 201


@app.route("/jokes/<int:joke_id>/vote", methods=["POST"])
def vote_for_joke(joke_id):
    payload = request.get_json(silent=True) or {}
    vote_value = str(payload.get("vote", "")).strip().lower()

    if vote_value not in {"up", "down"}:
        return error('Vote must be "up" or "down"', 400)

    updated = vote_joke(joke_id, vote_value)
    if updated is None:
        return error("Joke not found", 404)

    return jsonify(updated), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)