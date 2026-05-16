from flask import Flask, request, jsonify

app = Flask(__name__)

quotes = [
    {"id": 1, "text": "Я мыслю, следовательно, я существую.", "author": "Рене Декарт", "tags": ["philosophy", "life"]}
]
next_id = 2

@app.route('/quotes', methods=['GET'])
def get_quotes():
    return jsonify(quotes)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)