import http.server
import json
import os
import string
import random
import re
from datetime import datetime
from urllib.parse import urlparse

PORT = int(os.getenv('PORT', 5000))
DATA_FILE = os.getenv('DATA_FILE', '/data/links.json')

# Загружаем данные из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Сохраняем данные в файл
def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Генерируем случайный код из 4 символов
def generate_code(data, length=4):
    chars = string.ascii_letters + string.digits  # a-zA-Z0-9
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if code not in data:
            return code

class Handler(http.server.BaseHTTPRequestHandler):
    
    def send_json(self, data, status=200):
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def do_POST(self):
        if self.path == '/shorten':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                req = json.loads(body)
                if 'url' not in req:
                    return self.send_json({'error': 'URL is required'}, 400)
                
                data = load_data()
                code = generate_code(data)
                data[code] = {
                    'url': req['url'],
                    'created_at': datetime.utcnow().isoformat(),
                    'views': 0
                }
                save_data(data)
                return self.send_json({'code': code}, 201)
            except json.JSONDecodeError:
                return self.send_json({'error': 'Invalid JSON'}, 400)
        self.send_error(404)
    
    def do_GET(self):
        # Редирект: /r/{code}
        m = re.match(r'^/r/([a-zA-Z0-9]+)$', self.path)
        if m:
            code = m.group(1)
            data = load_data()
            if code not in data:
                return self.send_json({'error': 'Not found'}, 404)
            
            # Увеличиваем счётчик просмотров
            data[code]['views'] += 1
            save_data(data)
            
            self.send_response(302)
            self.send_header('Location', data[code]['url'])
            self.end_headers()
            return
        
        # Статистика: /stats/{code}
        m = re.match(r'^/stats/([a-zA-Z0-9]+)$', self.path)
        if m:
            code = m.group(1)
            data = load_data()
            if code not in data:
                return self.send_json({'error': 'Not found'}, 404)
            
            entry = data[code]
            return self.send_json({
                'code': code,
                'original_url': entry['url'],
                'created_at': entry['created_at'],
                'views': entry['views']
            })
        
        # Health check
        if self.path == '/health':
            return self.send_json({'status': 'ok'})
        
        self.send_error(404)
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

if __name__ == '__main__':
    print(f"🚀 Server started on http://localhost:{PORT}")
    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    server.serve_forever()