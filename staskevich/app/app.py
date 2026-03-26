from flask import Flask, jsonify, request

app = Flask(__name__)

scores = []
next_id = 1


def validate_score_payload(data):
    if not isinstance(data, dict):
        return "Тело запроса должно быть JSON-объектом."

    required_fields = ["player", "game", "score"]
    for field in required_fields:
        if field not in data:
            return f"Отсутствует обязательное поле: {field}"

    if not isinstance(data["player"], str) or not data["player"].strip():
        return "Поле 'player' должно быть непустой строкой."

    if not isinstance(data["game"], str) or not data["game"].strip():
        return "Поле 'game' должно быть непустой строкой."

    if not isinstance(data["score"], int) or data["score"] < 0:
        return "Поле 'score' должно быть неотрицательным целым числом."

    return None


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Scoreboard API is running",
        "endpoints": {
            "POST /scores": {
                "body": {
                    "player": "madmax",
                    "game": "digdug",
                    "score": 751300
                }
            },
            "GET /scores/top?game=digdug&limit=10": "Top scores by game",
            "GET /scores/player/<name>": "Scores by player"
        }
    })


@app.route("/scores", methods=["POST"])
def create_score():
    global next_id

    data = request.get_json(silent=True)
    error = validate_score_payload(data)
    if error:
        return jsonify({"error": error}), 400

    score_record = {
        "id": next_id,
        "player": data["player"].strip(),
        "game": data["game"].strip(),
        "score": data["score"]
    }

    scores.append(score_record)
    next_id += 1

    return jsonify(score_record), 201


@app.route("/scores/top", methods=["GET"])
def get_top_scores():
    game = request.args.get("game", "").strip()
    limit_raw = request.args.get("limit", "10").strip()

    if not game:
        return jsonify({"error": "Параметр 'game' обязателен."}), 400

    try:
        limit = int(limit_raw)
        if limit <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Параметр 'limit' должен быть положительным целым числом."}), 400

    filtered_scores = [item for item in scores if item["game"] == game]
    sorted_scores = sorted(filtered_scores, key=lambda item: item["score"], reverse=True)

    return jsonify(sorted_scores[:limit])


@app.route("/scores/player/<name>", methods=["GET"])
def get_player_scores(name):
    player_scores = [item for item in scores if item["player"] == name]
    return jsonify(player_scores)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
