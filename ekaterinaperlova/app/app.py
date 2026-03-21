from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = '/data/habits.db'  # Путь, где будет храниться база внутри контейнера

def init_db():
    """Инициализация базы данных"""
    os.makedirs('/data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            check_date DATE NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id),
            UNIQUE(habit_id, check_date)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/habits', methods=['GET'])
def get_habits():
    conn = get_db()
    habits = conn.execute('SELECT * FROM habits').fetchall()
    conn.close()
    return jsonify([dict(h) for h in habits])

@app.route('/habits', methods=['POST'])
def create_habit():
    data = request.get_json()
    if not data or 'name' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing name or user_id'}), 400
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO habits (name, user_id) VALUES (?, ?)',
        (data['name'], data['user_id'])
    )
    conn.commit()
    new_habit = conn.execute('SELECT * FROM habits WHERE id = ?', (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(new_habit)), 201

@app.route('/habits/<int:habit_id>/check', methods=['POST'])
def check_habit(habit_id):
    data = request.get_json()
    if not data or 'date' not in data:
        return jsonify({'error': 'Missing date'}), 400
    try:
        check_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    conn = get_db()
    habit = conn.execute('SELECT * FROM habits WHERE id = ?', (habit_id,)).fetchone()
    if not habit:
        conn.close()
        return jsonify({'error': 'Habit not found'}), 404

    try:
        conn.execute(
            'INSERT INTO checks (habit_id, check_date) VALUES (?, ?)',
            (habit_id, check_date.isoformat())
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Check recorded successfully'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Check already exists for this date'}), 400

@app.route('/habits/<int:habit_id>/streak', methods=['GET'])
def get_streak(habit_id):
    conn = get_db()
    habit = conn.execute('SELECT * FROM habits WHERE id = ?', (habit_id,)).fetchone()
    if not habit:
        conn.close()
        return jsonify({'error': 'Habit not found'}), 404

    checks = conn.execute(
        'SELECT check_date FROM checks WHERE habit_id = ? ORDER BY check_date DESC',
        (habit_id,)
    ).fetchall()
    conn.close()

    if not checks:
        return jsonify({'streak': 0})

    streak = 1
    last_date = datetime.strptime(checks[0]['check_date'], '%Y-%m-%d').date()
    today = datetime.now().date()

    if (today - last_date).days > 1:
        return jsonify({'streak': 0})

    for i in range(1, len(checks)):
        current_date = datetime.strptime(checks[i]['check_date'], '%Y-%m-%d').date()
        prev_date = datetime.strptime(checks[i-1]['check_date'], '%Y-%m-%d').date()
        if (prev_date - current_date).days == 1:
            streak += 1
        else:
            break
    return jsonify({'streak': streak})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)