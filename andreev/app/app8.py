from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище: словарь, где ключ - id, значение - данные изображения
images_db = {}
next_id = 1


@app.route('/images', methods=['POST'])
def create_image():
    """Создание нового изображения"""
    global next_id
    
    data = request.get_json()
    
    # Валидация обязательных полей
    if not data or 'url' not in data or 'width' not in data or 'height' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Создаем запись
    image = {
        'id': next_id,
        'url': data['url'],
        'width': data['width'],
        'height': data['height'],
        'tags': data.get('tags', [])  # tags опциональны
    }
    
    images_db[next_id] = image
    next_id += 1
    
    return jsonify(image), 201


@app.route('/images', methods=['GET'])
def get_images():
    """Получение списка изображений с фильтрацией по тегу"""
    tag = request.args.get('tag')
    
    if tag:
        # Фильтруем по тегу
        filtered = [img for img in images_db.values() if tag in img['tags']]
        return jsonify(filtered)
    
    # Возвращаем все изображения
    return jsonify(list(images_db.values()))


@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    """Получение деталей конкретного изображения"""
    image = images_db.get(image_id)
    
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    return jsonify(image)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)