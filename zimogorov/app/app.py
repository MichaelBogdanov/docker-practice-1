import json
import random
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

quotes = []
next_id = 1

@app.route('/')
def index():
    return jsonify({"message": "Quotes API. см. /quotes"})

@app.route('/quotes', methods=['GET'])
def get_quotes():
    tag = request.args.get('tag')
    limit = request.args.get('limit', default=None, type=int)

    result = quotes.copy()
    if tag:
        result = [q for q in result if tag in q['tags']]
    if limit and limit > 0:
        result = result[:limit]

    return jsonify(result)

@app.route('/quotes/random', methods=['GET'])
def random_quote():
    tag = request.args.get('tag')
    filtered = quotes.copy()
    if tag:
        filtered = [q for q in filtered if tag in q['tags']]
    if not filtered:
        return jsonify({"error": "Не найдено"}), 404
    return jsonify(random.choice(filtered))

@app.route('/quotes', methods=['POST'])
def add_quote():
    data = request.get_json()
    if not data or 'text' not in data or 'author' not in data:
        return jsonify({"error": "пропущен 'text' или 'author'"}), 400
    if 'tags' not in data or not isinstance(data['tags'], list):
        data['tags'] = []

    global next_id
    new_quote = {
        "id": next_id,
        "text": data['text'],
        "author": data['author'],
        "tags": data['tags']
    }
    quotes.append(new_quote)
    next_id += 1
    return jsonify(new_quote), 201

@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    global quotes
    for i, q in enumerate(quotes):
        if q['id'] == quote_id:
            del quotes[i]
            return jsonify({"message": "удалена"}), 200
    return jsonify({"error": "Не найдено"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)