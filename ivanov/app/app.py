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
# Добавление отчёта о погоде
@app.route('/reports', methods=['POST'])
def create_report():
    try:
        data = request.get_json()
        
        # Проверка обязательных полей
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if not 'city' in data:
            return jsonify({'error': 'City is required'}), 400

        if not 'text' in data:
            return jsonify({'error': 'Text is required'}), 400

        if not 'temp' in data:
            return jsonify({'error': 'Temperature is required'}), 400
        

        # Получение данных
        city = data['city']
        text = data['text']
        temp = data['temp']
        
        db = get_db()
        cursor = db.cursor()
        
        # SQL запрос для вставки данных
        cursor.execute('''
            INSERT INTO reports (city, text, temp, timestamp)
            VALUES (?, ?, ?, datetime('now'))
        ''', (city, text, temp))
        
        db.commit()
        
        # Возвращаем ответ
        return jsonify({
            'id': cursor.lastrowid,
            'city': city,
            'text': text,
            'temp': temp,
            'message': 'Report created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Просмотр всех отчётов
@app.route('/reports', methods=['GET'])
def get_reports():
    try:
        city = request.args.get('city')
        db = get_db()
        cursor = db.cursor()
        
        # SQL запрос с возможной фильтрацией по городу
        if city:
            cursor.execute('''
                SELECT id, city, text, temp, timestamp
                FROM reports
                WHERE city = ?
                ORDER BY timestamp DESC
            ''', (city,))
        else:
            cursor.execute('''
                SELECT id, city, text, temp, timestamp
                FROM reports
                ORDER BY timestamp DESC
            ''')
        
        reports = cursor.fetchall()
        
        # Преобразуем результы в список словарей
        result = []
        for report in reports:
            result.append({
                'id': report['id'],
                'city': report['city'],
                'text': report['text'],
                'temp': report['temp'],
                'timestamp': report['timestamp']
            })

        # Если данных нет, возвращаем ошибку
        if not result:
            return jsonify({'message': 'No reports found'}), 404
        
        # Возвращаем результаты
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Запускаем приложение
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)