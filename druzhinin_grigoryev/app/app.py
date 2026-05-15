from flask import Flask, request, jsonify, redirect
import redis
import string
import random
from datetime import datetime
import os

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    decode_responses=True
)

def generate_code(length=4):
    """Генерация уникального кода для ссылки"""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not redis_client.exists(f"url:{code}"):
            return code

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Создание короткой ссылки"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    original_url = data['url']
    
    code = generate_code()
    
    redis_client.set(f"url:{code}", original_url)
    redis_client.hset(f"stats:{code}", mapping={
        'created_at': datetime.now().isoformat(),
        'views': 0
    })
    
    return jsonify({'code': code}), 201

@app.route('/r/<code>', methods=['GET'])
def redirect_to_url(code):
    """Редирект по короткому коду"""
    original_url = redis_client.get(f"url:{code}")
    
    if not original_url:
        return jsonify({'error': 'Short URL not found'}), 404
    
    redis_client.hincrby(f"stats:{code}", 'views', 1)
    
    return redirect(original_url, code=302)

@app.route('/stats/<code>', methods=['GET'])
def get_stats(code):
    """Получение статистики по коду"""
    if not redis_client.exists(f"url:{code}"):
        return jsonify({'error': 'Short URL not found'}), 404
    
    stats = redis_client.hgetall(f"stats:{code}")
    
    return jsonify({
        'code': code,
        'created_at': stats.get('created_at'),
        'views': int(stats.get('views', 0)),
        'original_url': redis_client.get(f"url:{code}")
    })

@app.route('/health', methods=['GET'])
def health():
    """Проверка работоспособности"""
    try:
        redis_client.ping()
        return jsonify({'status': 'ok', 'redis': 'connected'})
    except:
        return jsonify({'status': 'error', 'redis': 'disconnected'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)