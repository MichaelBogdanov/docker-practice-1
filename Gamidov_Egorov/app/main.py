from flask import Flask, request, jsonify
import random

app = Flask(__name__)


quotes = [
    {
        "id": 1,
        "text": "The only limit is your mind.",
        "author": "Anonymous",
        "tags": ["life", "motivation"]
    },
    {
        "id": 2,
        "text": "Stay hungry, stay foolish.",
        "author": "Steve Jobs",
        "tags": ["life", "wisdom"]
    }
]
next_id = 3

def quote_to_dict(quote):
    return {
        "id": quote["id"],
        "text": quote["text"],
        "author": quote["author"],
        "tags": quote["tags"]
    }

@app.route('/quotes', methods=['GET'])
def get_quotes():
    tag = request.args.get('tag')
    limit = request.args.get('limit', default=None, type=int)
    
    result = quotes
    if tag:
        result = [q for q in result if tag in q["tags"]]
    if limit:
        result = result[:limit]
    
    return jsonify([quote_to_dict(q) for q in result])

@app.route('/quotes/random', methods=['GET'])
def random_quote():
    tag = request.args.get('tag')
    candidates = quotes
    if tag:
        candidates = [q for q in candidates if tag in q["tags"]]
    if not candidates:
        return jsonify({"error": "No quotes found with this tag"}), 404
    chosen = random.choice(candidates)
    return jsonify(quote_to_dict(chosen))

@app.route('/quotes', methods=['POST'])
def add_quote():
    global next_id
    data = request.get_json()
    
    if not data or 'text' not in data or 'author' not in data:
        return jsonify({"error": "Missing required fields: text, author"}), 400
    
    new_quote = {
        "id": next_id,
        "text": data["text"],
        "author": data["author"],
        "tags": data.get("tags", [])
    }
    quotes.append(new_quote)
    next_id += 1
    return jsonify(quote_to_dict(new_quote)), 201

@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    global quotes
    for i, q in enumerate(quotes):
        if q["id"] == quote_id:
            quotes.pop(i)
            return jsonify({"message": "Quote deleted"}), 200
    return jsonify({"error": "Quote not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)