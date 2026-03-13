from flask import Flask, request, jsonify
import random

app = Flask(__name__)

jokes = []
next_id = 1

@app.route("/jokes", methods=["GET"])
def get_jokes():
    category = request.args.get("category")
    if category:
        return jsonify([j for j in jokes if j["category"] == category])
    return jsonify(jokes)

@app.route("/jokes/random", methods=["GET"])
def get_random_joke():
    category = request.args.get("category")
    filtered = [j for j in jokes if (j["category"] == category if category else True)]
    if not filtered:
        return jsonify({"error": "No jokes found"}), 404
    return jsonify(random.choice(filtered))

@app.route("/jokes", methods=["POST"])
def add_joke():
    global next_id
    data = request.get_json()
    joke = {
        "id": next_id,
        "text": data["text"],
        "category": data["category"],
        "votes": 0
    }
    jokes.append(joke)
    next_id += 1
    return jsonify(joke), 201

@app.route("/jokes/<int:joke_id>/vote", methods=["POST"])
def vote_joke(joke_id):
    data = request.get_json()
    for joke in jokes:
        if joke["id"] == joke_id:
            if data["vote"] == "up":
                joke["votes"] += 1
            elif data["vote"] == "down":
                joke["votes"] -= 1
            return jsonify(joke)
    return jsonify({"error": "Joke not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)