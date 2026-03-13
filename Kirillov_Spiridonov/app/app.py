from flask import Flask, request, jsonify
import random

app = Flask(__name__)

jokes = []
joke_id = 1

@app.route("/jokes", methods=["GET"])
def get_jokes():
    return jsonify(jokes)

@app.route("/jokes", methods=["POST"])
def add_joke():
    global joke_id
    data = request.json
    joke = {"id": joke_id, "text": data["text"], "category": data["category"], "votes": 0}
    jokes.append(joke)
    joke_id += 1
    return jsonify(joke)

@app.route("/jokes/<int:id>/vote", methods=["POST"])
def vote_joke(id):
    data = request.json
    for joke in jokes:
        if joke["id"] == id:
            if data["vote"] == "up":
                joke["votes"] += 1
            elif data["vote"] == "down":
                joke["votes"] -= 1
            return jsonify(joke)
    return jsonify({"error": "Joke not found"}), 404

app.run(host="0.0.0.0", port=5000)