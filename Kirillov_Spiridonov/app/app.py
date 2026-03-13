from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# =========================
# 1) шутки API (3 задание)
# =========================
jokes = []
next_joke_id = 1

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
    global next_joke_id
    data = request.get_json()
    joke = {
        "id": next_joke_id,
        "text": data["text"],
        "category": data["category"],
        "votes": 0
    }
    jokes.append(joke)
    next_joke_id += 1
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

# =========================
# 2) таблица рекордов API (9 задание)
# =========================
scores = []

@app.route("/scores", methods=["POST"])
def add_score():
    data = request.get_json()
    scores.append(data)
    return jsonify(data), 201

@app.route("/scores/top", methods=["GET"])
def top_scores():
    game = request.args.get("game")
    limit = int(request.args.get("limit", 10))
    filtered = [s for s in scores if s["game"] == game]
    sorted_scores = sorted(filtered, key=lambda x: x["score"], reverse=True)
    return jsonify(sorted_scores[:limit])

@app.route("/scores/player/<name>", methods=["GET"])
def player_scores(name):
    filtered = [s for s in scores if s["player"] == name]
    return jsonify(filtered)

# =========================
# 3) растения API (11 задание)
# =========================
plants = []
next_plant_id = 1

@app.route("/plants", methods=["POST"])
def add_plant():
    global next_plant_id
    data = request.get_json()
    plant = {
        "id": next_plant_id,
        "name": data["name"],
        "water_interval_days": data["water_interval_days"],
        "last_watered": None
    }
    plants.append(plant)
    next_plant_id += 1
    return jsonify(plant), 201

@app.route("/plants/<int:plant_id>/water", methods=["POST"])
def water_plant(plant_id):
    data = request.get_json()
    for plant in plants:
        if plant["id"] == plant_id:
            plant["last_watered"] = datetime.strptime(data["date"], "%Y-%m-%d")
            return jsonify(plant)
    return jsonify({"error": "Plant not found"}), 404

@app.route("/plants/<int:plant_id>/status", methods=["GET"])
def plant_status(plant_id):
    for plant in plants:
        if plant["id"] == plant_id:
            if plant["last_watered"]:
                days = (datetime.now() - plant["last_watered"]).days
            else:
                days = None
            need_water = (days is None) or (days >= plant["water_interval_days"])
            return jsonify({"days_since_water": days, "need_water": need_water})
    return jsonify({"error": "Plant not found"}), 404

# =========================
# Run server
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)