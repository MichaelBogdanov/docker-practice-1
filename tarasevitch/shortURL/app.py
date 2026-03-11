import random
import string
from datetime import datetime
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)


links = {}


def generate_code(length=4):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json(silent=True)

    if not data or "url" not in data:
        return jsonify({"error": "url is required"}), 400

    url = data["url"].strip()

    if not url:
        return jsonify({"error": "url is empty"}), 400

    code = generate_code()
    while code in links:
        code = generate_code()

    links[code] = {
        "url": url,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 0
    }

    return jsonify({"code": code}), 200


@app.route("/r/<code>", methods=["GET"])
def redirect_to_url(code):
    if code not in links:
        return jsonify({"error": "code not found"}), 404

    links[code]["views"] += 1
    return redirect(links[code]["url"], code=302)


@app.route("/stats/<code>", methods=["GET"])
def stats(code):
    if code not in links:
        return jsonify({"error": "code not found"}), 404

    return jsonify({
        "code": code,
        "url": links[code]["url"],
        "created_at": links[code]["created_at"],
        "views": links[code]["views"]
    }), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "URL shortener API running",
        "endpoints": {
            "POST /shorten": "create short link",
            "GET /r/<code>": "redirect to original URL",
            "GET /stats/<code>": "show statistics"
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
