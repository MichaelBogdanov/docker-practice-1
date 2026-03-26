from flask import Flask, request, jsonify
import random

app = Flask(__name__)

quotes = []
tasks = []
scores = []

qid = 1
tid = 1
sid = 1

# ---- QUOTES ----
@app.route("/quotes", methods=["GET"])
def get_quotes():
    tag = request.args.get("tag")
    res = quotes
    if tag:
        res = [q for q in res if tag in q["tags"]]
    return jsonify(res)

@app.route("/quotes/random", methods=["GET"])
def random_quote():
    if not quotes:
        return jsonify({"error": "no quotes"})
    return jsonify(random.choice(quotes))

@app.route("/quotes", methods=["POST"])
def add_quote():
    global qid
    data = request.json
    q = {"id": qid, "text": data["text"], "author": data["author"], "tags": data["tags"]}
    qid += 1
    quotes.append(q)
    return jsonify(q)

@app.route("/quotes/<int:id>", methods=["DELETE"])
def del_quote(id):
    global quotes
    quotes = [q for q in quotes if q["id"] != id]
    return jsonify({"ok": True})


# ---- TASKS ----
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    global tid
    data = request.json
    t = {"id": tid, "title": data["title"], "due": data["due"], "priority": data["priority"], "status": "open"}
    tid += 1
    tasks.append(t)
    return jsonify(t)

@app.route("/tasks/<int:id>", methods=["PATCH"])
def upd_task(id):
    data = request.json
    for t in tasks:
        if t["id"] == id:
            t.update(data)
    return jsonify({"ok": True})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def del_task(id):
    global tasks
    tasks = [t for t in tasks if t["id"] != id]
    return jsonify({"ok": True})


# ---- SCORES ----
@app.route("/scores", methods=["POST"])
def add_score():
    global sid
    data = request.json
    s = {"id": sid, "player": data["player"], "game": data["game"], "score": data["score"]}
    sid += 1
    scores.append(s)
    return jsonify(s)

@app.route("/scores/top", methods=["GET"])
def top_scores():
    game = request.args.get("game")
    res = [s for s in scores if s["game"] == game] if game else scores
    res = sorted(res, key=lambda x: x["score"], reverse=True)
    return jsonify(res[:10])

@app.route("/scores/player/<name>", methods=["GET"])
def player_scores(name):
    return jsonify([s for s in scores if s["player"] == name])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)