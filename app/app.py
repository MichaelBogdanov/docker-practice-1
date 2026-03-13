from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = '/data/images.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            tags TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def dict_factory(cursor, row):
#преобразование строки бд в словарь
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/images', methods=['POST'])
def create_image():

    try:
        data = request.get_json()
        
        #валидация полей
        if not all(k in data for k in ('url', 'width', 'height')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        #преобразуем список тегов в строку для хранения бд
        tags = data.get('tags', [])
        tags_str = ','.join(tags) if tags else ''
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO images (url, width, height, tags) VALUES (?, ?, ?, ?)',
            (data['url'], data['width'], data['height'], tags_str)
        )
        conn.commit()
        
        image_id = cursor.lastrowid
        cursor.execute('SELECT * FROM images WHERE id = ?', (image_id,))
        image = cursor.fetchone()
        conn.close()
        
        #теги обратно в список
        if image and image[4]:
            image_dict = {
                'id': image[0],
                'url': image[1],
                'width': image[2],
                'height': image[3],
                'tags': image[4].split(',') if image[4] else [],
                'created_at': image[5]
            }
        else:
            image_dict = None
        
        return jsonify(image_dict), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/images', methods=['GET'])
def get_images():
    #список изображений с фильтрацией
    try:
        tag_filter = request.args.get('tag')
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        if tag_filter:
            #ищем по тегам
            cursor.execute(
                'SELECT * FROM images WHERE tags LIKE ?',
                (f'%{tag_filter}%',)
            )
        else:
            cursor.execute('SELECT * FROM images ORDER BY created_at DESC')
        
        images = cursor.fetchall()
        conn.close()
        
        #преобразуем теги в список для изображения
        for image in images:
            if image['tags']:
                image['tags'] = image['tags'].split(',')
            else:
                image['tags'] = []
        
        return jsonify(images)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM images WHERE id = ?', (image_id,))
        image = cursor.fetchone()
        conn.close()
        
        if image is None:
            return jsonify({'error': 'Image not found'}), 404
        
        #теги из строки в список
        if image['tags']:
            image['tags'] = image['tags'].split(',')
        else:
            image['tags'] = []
        
        return jsonify(image)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    os.makedirs('/data', exist_ok=True)
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)