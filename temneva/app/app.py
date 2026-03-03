from flask import Flask, request, jsonify

app = Flask(__name__)

images = []
next_id = 1

@app.route('/images', methods=['POST'])
def create_image():
    # Добавление нового изображения
    global next_id
    data = request.get_json()
    
    # Проверка обязательного поля url
    if not data or 'url' not in data:
        return jsonify({'error': 'url is required'}), 400
    
    # Создание
    image = {
        'id': next_id,
        'url': data['url'],
        'width': data.get('width'),
        'height': data.get('height'),
        'tags': data.get('tags', [])
    }
    
    images.append(image)
    next_id += 1
    
    return jsonify(image), 201

@app.route('/images', methods=['GET'])
def get_images():
    # Получение списка с фильтром по тегу
    tag = request.args.get('tag')
    
    if tag:
        result = [img for img in images if tag in img.get('tags', [])]
        return jsonify(result)
    
    return jsonify(images)

@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    # Получение одного изображения по ID
    for img in images:
        if img['id'] == image_id:
            return jsonify(img)
    
    return jsonify({'error': 'not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)