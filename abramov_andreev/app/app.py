from flask import Flask, request, jsonify

app = Flask(__name__)

images = []
next_id = 1


@app.route("/images", methods=["POST"])
def create_image():
    global next_id

    data = request.json

    image = {
        "id": next_id,
        "url": data["url"],
        "width": data["width"],
        "height": data["height"],
        "tags": data.get("tags", [])
    }

    images.append(image)
    next_id += 1

    return jsonify(image), 201


@app.route("/images", methods=["GET"])
def get_images():
    tag = request.args.get("tag")

    if tag:
        filtered = [img for img in images if tag in img["tags"]]
        return jsonify(filtered)

    return jsonify(images)


@app.route("/images/<int:image_id>", methods=["GET"])
def get_image(image_id):
    for img in images:
        if img["id"] == image_id:
            return jsonify(img)

    return jsonify({"error": "Image not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
