from flask import Flask, request, jsonify

app = Flask(__name__)

images = []
next_id = 1


@app.route("/images", methods=["POST"])
def create_image():
    global next_id

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    required_fields = ["url", "width", "height", "tags"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    url = str(data["url"]).strip()
    width = data["width"]
    height = data["height"]
    tags = data["tags"]

    if not url:
        return jsonify({"error": "url is empty"}), 400

    if not isinstance(width, int) or width <= 0:
        return jsonify({"error": "width must be a positive integer"}), 400

    if not isinstance(height, int) or height <= 0:
        return jsonify({"error": "height must be a positive integer"}), 400

    if not isinstance(tags, list):
        return jsonify({"error": "tags must be a list"}), 400

    clean_tags = [str(tag).strip() for tag in tags if str(tag).strip()]

    image = {
        "id": next_id,
        "url": url,
        "width": width,
        "height": height,
        "tags": clean_tags
    }

    images.append(image)
    next_id += 1

    return jsonify(image), 201


@app.route("/images", methods=["GET"])
def get_images():
    tag = request.args.get("tag")

    if tag:
        filtered = [image for image in images if tag in image["tags"]]
        return jsonify(filtered), 200

    return jsonify(images), 200


@app.route("/images/<int:image_id>", methods=["GET"])
def get_image_details(image_id):
    for image in images:
        if image["id"] == image_id:
            return jsonify(image), 200

    return jsonify({"error": "image not found"}), 404


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Image metadata API running",
        "endpoints": {
            "POST /images": "create image metadata",
            "GET /images": "list all images",
            "GET /images?tag=landscape": "filter images by tag",
            "GET /images/<id>": "get image details"
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
