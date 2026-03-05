from flask import Flask, request, jsonify, g
import sqlite3
import json
from datetime import datetime

# ==== Конфигурация ==== #
DEBUG = True
PORT = 5000
DATABASE_PATH = 'weater_reposts.db'
# ==== Конфигурация ==== #

# Создаём приложение
app = Flask(__name__)

# Подключение к базе данных
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db

# Закрытие соединения с базой данных
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Инициализация таблицы
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                text TEXT NOT NULL,
                temp INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

# Инициализация базы данных при первом запросе
@app.before_request
def before_request():
    init_db()

# Маршрутизация
# TODO

# Запускаем приложение
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)