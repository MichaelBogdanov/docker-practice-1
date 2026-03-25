import sqlite3
from datetime import date
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
DB = '/data/plants.db'


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                water_interval_days INTEGER NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS waterings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (plant_id) REFERENCES plants(id)
            )
        ''')


init_db()


@app.route('/plants', methods=['GET'])
def list_plants():
    with get_db() as conn:
        plants = conn.execute('SELECT * FROM plants').fetchall()
    return jsonify([dict(p) for p in plants])


@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json(force=True)
    name = data.get('name')
    interval = data.get('water_interval_days')
    if not name or interval is None:
        abort(400)
    with get_db() as conn:
        cur = conn.execute(
            'INSERT INTO plants (name, water_interval_days) VALUES (?, ?)',
            (name, int(interval))
        )
        plant = conn.execute('SELECT * FROM plants WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(dict(plant)), 201


@app.route('/plants/<int:plant_id>/water', methods=['POST'])
def water_plant(plant_id):
    data = request.get_json(force=True)
    date_str = data.get('date', date.today().isoformat())
    with get_db() as conn:
        if not conn.execute('SELECT id FROM plants WHERE id = ?', (plant_id,)).fetchone():
            abort(404)
        conn.execute(
            'INSERT INTO waterings (plant_id, date) VALUES (?, ?)',
            (plant_id, date_str)
        )
    return jsonify({'plant_id': plant_id, 'date': date_str}), 201


@app.route('/plants/<int:plant_id>/status', methods=['GET'])
def plant_status(plant_id):
    with get_db() as conn:
        plant = conn.execute('SELECT * FROM plants WHERE id = ?', (plant_id,)).fetchone()
        if not plant:
            abort(404)
        last = conn.execute(
            'SELECT date FROM waterings WHERE plant_id = ? ORDER BY date DESC LIMIT 1',
            (plant_id,)
        ).fetchone()

    if last:
        days_since = (date.today() - date.fromisoformat(last['date'])).days
    else:
        days_since = None

    return jsonify({
        'plant_id': plant_id,
        'name': plant['name'],
        'water_interval_days': plant['water_interval_days'],
        'days_since_water': days_since,
        'need_water': days_since is None or days_since >= plant['water_interval_days']
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
