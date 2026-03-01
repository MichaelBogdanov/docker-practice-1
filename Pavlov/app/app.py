import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

def db_connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
    )

def create_table_if_not_exists():
    conn = db_connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id SERIAL PRIMARY KEY,
            player VARCHAR(100) NOT NULL,
            game   VARCHAR(100) NOT NULL,
            score  INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

create_table_if_not_exists()

@app.route("/scores", methods=["POST"])
def add_score():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body"}), 400

    player = data.get("player")
    game = data.get("game")
    score = data.get("score")

    if not player or not game or score is None:
        return jsonify({"error": "Missing fields: player, game, score"}), 400

    conn = db_connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO scores (player, game, score) VALUES (%s, %s, %s) RETURNING id",
        (player, game, score),
    )
    new_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": new_id,
        "player": player,
        "game": game,
        "score": score
    }), 201

@app.route("/scores/top", methods=["GET"])
def get_top_scores():
    game = request.args.get("game")
    limit = request.args.get("limit", default=10, type=int)

    if not game:
        return jsonify({"error": "Missing query parameter: game"}), 400

    conn = db_connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT player, game, score
        FROM scores
        WHERE game = %s
        ORDER BY score DESC
        LIMIT %s
        """,
        (game, limit),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows), 200

@app.route("/scores/player/<name>", methods=["GET"])
def get_player_scores(name):
    conn = db_connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT player, game, score
        FROM scores
        WHERE player = %s
        ORDER BY score DESC
        """,
        (name,),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
