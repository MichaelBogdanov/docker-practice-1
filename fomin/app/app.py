import random
from flask import Flask, request, jsonify

app = Flask(__name__)

quotes = [
    {"id": 1, "text": "Я мыслю, следовательно, я существую.", "author": "Рене Декарт", "tags": ["philosophy", "life"]}
]
next_id = 2

@app.route('/quotes', methods=['GET'])
def get_quotes():
    tag = request.args.get('tag')
    limit = request.args.get('limit', type=int)

    result = quotes
    if tag:
        result = [q for q in result if tag in q.get('tags', [])]
    if limit:
        result = result[:limit]

    return jsonify(result)

@app.route('/quotes/random', methods=['GET'])
def get_random_quote():
    tag = request.args.get('tag')

    result = quotes
    if tag:
        result = [q for q in result if tag in q.get('tags', [])]

    if not result:
        return jsonify({"error": "Цитаты не найдены"}), 404

    return jsonify(random.choice(result))

@app.route('/quotes', methods=['POST'])
def add_quote():
    global next_id
    data = request.json
    new_quote = {
        "id": next_id,
        "text": data.get("text", ""),
        "author": data.get("author", "Неизвестный"),
        "tags": data.get("tags", [])
    }
    quotes.append(new_quote)
    next_id += 1
    return jsonify(new_quote), 201

@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    global quotes
    quotes = [q for q in quotes if q["id"] != quote_id]
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)