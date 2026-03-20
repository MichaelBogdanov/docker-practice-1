import sqlite3
import random
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_PATH = '/app/data/jokes.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    return conn

@app.route('/jokes', methods=['GET'])
def list_jokes():
    category = request.args.get('category')
    conn = get_db()
    if category:
        jokes = conn.execute('SELECT * FROM jokes WHERE category = ? ORDER BY id', (category,)).fetchall()
    else:
        jokes = conn.execute('SELECT * FROM jokes ORDER BY id').fetchall()
    conn.close()
    return jsonify([dict(row) for row in jokes])

@app.route('/jokes/random', methods=['GET'])
def random_joke():
    category = request.args.get('category')
    conn = get_db()
    if category:
        jokes = conn.execute('SELECT * FROM jokes WHERE category = ?', (category,)).fetchall()
    else:
        jokes = conn.execute('SELECT * FROM jokes').fetchall()
    conn.close()
    if not jokes:
        return jsonify({'error': 'No jokes found'}), 404
    chosen = random.choice(jokes)
    return jsonify(dict(chosen))

@app.route('/jokes', methods=['POST'])
def add_joke():
    data = request.get_json()
    if not data or 'text' not in data or 'category' not in data:
        return jsonify({'error': 'Missing text or category'}), 400
    text = data['text']
    category = data['category']
    conn = get_db()
    cursor = conn.execute('INSERT INTO jokes (text, category) VALUES (?, ?)', (text, category))
    conn.commit()
    joke_id = cursor.lastrowid
    new_joke = conn.execute('SELECT * FROM jokes WHERE id = ?', (joke_id,)).fetchone()
    conn.close()
    return jsonify(dict(new_joke)), 201

@app.route('/jokes/<int:joke_id>/vote', methods=['POST'])
def vote_joke(joke_id):
    data = request.get_json()
    if not data or 'vote' not in data:
        return jsonify({'error': 'Missing vote field'}), 400
    vote = data['vote'].lower()
    if vote not in ('up', 'down'):
        return jsonify({'error': 'Vote must be "up" or "down"'}), 400
    conn = get_db()
    joke = conn.execute('SELECT * FROM jokes WHERE id = ?', (joke_id,)).fetchone()
    if not joke:
        conn.close()
        return jsonify({'error': 'Joke not found'}), 404
    delta = 1 if vote == 'up' else -1
    conn.execute('UPDATE jokes SET votes = votes + ? WHERE id = ?', (delta, joke_id))
    conn.commit()
    updated_joke = conn.execute('SELECT * FROM jokes WHERE id = ?', (joke_id,)).fetchone()
    conn.close()
    return jsonify(dict(updated_joke))

if __name__ == '__main__':
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    app.run(host='0.0.0.0', port=5000)