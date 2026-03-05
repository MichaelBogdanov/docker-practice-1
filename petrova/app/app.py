#!/usr/bin/env python3
"""
API для шуток (jokes) с голосованием
"""

import sqlite3
import random
from flask import Flask, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

DATABASE = 'jokes.db'

def get_db():
    """Получение соединения с БД"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Закрытие соединения с БД"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Инициализация базы данных"""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
       
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                category TEXT NOT NULL,
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        
        cursor.execute("SELECT COUNT(*) as count FROM jokes")
        if cursor.fetchone()['count'] == 0:
            sample_jokes = [
                ("Why do programmers prefer dark mode?", "programming"),
                ("Because light attracts bugs!", "programming"),
                ("Что такое анекдот про Штирлица?", "cops"),
                ("Штирлиц шел по коридору и услышал выстрел. 'Стреляют', - подумал Штирлиц и выстрелил в ответ.", "cops"),
                ("2+2=5", "math"),
                ("Для очень больших значений 2", "math"),
            ]
            
            for text, category in sample_jokes:
                cursor.execute(
                    "INSERT INTO jokes (text, category) VALUES (?, ?)",
                    (text, category)
                )
        
        db.commit()

init_db()

@app.route('/jokes', methods=['GET'])
def get_jokes():
    """
    GET /jokes - список всех шуток
    GET /jokes?category=programming - фильтр по категории
    """
    category = request.args.get('category')
    
    db = get_db()
    cursor = db.cursor()
    
    if category:
        cursor.execute(
            "SELECT * FROM jokes WHERE category = ? ORDER BY created_at DESC",
            (category,)
        )
    else:
        cursor.execute("SELECT * FROM jokes ORDER BY created_at DESC")
    
    jokes = cursor.fetchall()
    

    result = []
    for joke in jokes:
        result.append({
            'id': joke['id'],
            'text': joke['text'],
            'category': joke['category'],
            'upvotes': joke['upvotes'],
            'downvotes': joke['downvotes'],
            'rating': joke['upvotes'] - joke['downvotes']
        })
    
    return jsonify(result)

@app.route('/jokes/random', methods=['GET'])
def get_random_joke():
    """
    GET /jokes/random - случайная шутка
    GET /jokes/random?category=math - случайная шутка из категории
    """
    category = request.args.get('category')
    
    db = get_db()
    cursor = db.cursor()
    
    if category:
        cursor.execute(
            "SELECT * FROM jokes WHERE category = ?",
            (category,)
        )
    else:
        cursor.execute("SELECT * FROM jokes")
    
    jokes = cursor.fetchall()
    
    if not jokes:
        return jsonify({'error': 'No jokes found'}), 404
    
  
    joke = random.choice(jokes)
    
    return jsonify({
        'id': joke['id'],
        'text': joke['text'],
        'category': joke['category'],
        'upvotes': joke['upvotes'],
        'downvotes': joke['downvotes'],
        'rating': joke['upvotes'] - joke['downvotes']
    })

@app.route('/jokes', methods=['POST'])
def add_joke():
    """
    POST /jokes - добавить новую шутку
    Тело запроса: {"text": "...", "category": "..."}
    """
    data = request.get_json()
    
    if not data or 'text' not in data or 'category' not in data:
        return jsonify({'error': 'Missing text or category'}), 400
    
    text = data['text'].strip()
    category = data['category'].strip().lower()
    
    if not text or not category:
        return jsonify({'error': 'Text and category cannot be empty'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute(
        "INSERT INTO jokes (text, category) VALUES (?, ?)",
        (text, category)
    )
    db.commit()
    
    joke_id = cursor.lastrowid
    
    return jsonify({
        'id': joke_id,
        'text': text,
        'category': category,
        'upvotes': 0,
        'downvotes': 0,
        'rating': 0,
        'message': 'Joke added successfully'
    }), 201

@app.route('/jokes/<int:joke_id>/vote', methods=['POST'])
def vote_joke(joke_id):
    """
    POST /jokes/{id}/vote - проголосовать за шутку
    Тело запроса: {"vote": "up"} или {"vote": "down"}
    """
    data = request.get_json()
    
    if not data or 'vote' not in data:
        return jsonify({'error': 'Missing vote parameter'}), 400
    
    vote = data['vote'].lower()
    if vote not in ['up', 'down']:
        return jsonify({'error': 'Vote must be "up" or "down"'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
   
    cursor.execute("SELECT * FROM jokes WHERE id = ?", (joke_id,))
    joke = cursor.fetchone()
    
    if not joke:
        return jsonify({'error': 'Joke not found'}), 404
    

    if vote == 'up':
        cursor.execute(
            "UPDATE jokes SET upvotes = upvotes + 1 WHERE id = ?",
            (joke_id,)
        )
    else:  # down
        cursor.execute(
            "UPDATE jokes SET downvotes = downvotes + 1 WHERE id = ?",
            (joke_id,)
        )
    
    db.commit()
    

    cursor.execute("SELECT * FROM jokes WHERE id = ?", (joke_id,))
    updated_joke = cursor.fetchone()
    
    return jsonify({
        'id': updated_joke['id'],
        'text': updated_joke['text'],
        'category': updated_joke['category'],
        'upvotes': updated_joke['upvotes'],
        'downvotes': updated_joke['downvotes'],
        'rating': updated_joke['upvotes'] - updated_joke['downvotes'],
        'message': f'Vote "{vote}" recorded'
    })

@app.route('/jokes/categories', methods=['GET'])
def get_categories():
    """GET /jokes/categories - список всех категорий"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT DISTINCT category FROM jokes ORDER BY category")
    categories = [row['category'] for row in cursor.fetchall()]
    
    return jsonify(categories)

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)