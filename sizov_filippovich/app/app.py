from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных (SQLite, файл хранится в папке /data внутри контейнера)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////data/images.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --- Модель таблицы ---
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    # Теги хранятся как строка через запятую: "landscape,portrait"
    tags = db.Column(db.String, default="")

    def to_dict(self):
        """Преобразует запись в словарь для JSON-ответа."""
        return {
            "id": self.id,
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "tags": self.tags.split(",") if self.tags else [],
        }


# Создаём таблицы при старте
with app.app_context():
    db.create_all()


# --- Endpoints ---

@app.route("/images", methods=["POST"])
def add_image():
    """Добавить новое изображение. Принимает JSON с url, width, height, tags."""
    data = request.get_json()

    # Проверяем обязательные поля
    if not data or not data.get("url"):
        return jsonify({"error": "Поле url обязательно"}), 400

    image = Image(
        url=data["url"],
        width=data.get("width", 0),
        height=data.get("height", 0),
        tags=",".join(data.get("tags", [])),  # список -> строка
    )
    db.session.add(image)
    db.session.commit()

    return jsonify(image.to_dict()), 201


@app.route("/images", methods=["GET"])
def get_images():
    """Получить все изображения. Можно фильтровать по тегу: ?tag=landscape"""
    tag = request.args.get("tag")  # берём параметр из URL

    if tag:
        # Ищем те записи, где в поле tags есть нужный тег
        images = Image.query.filter(Image.tags.contains(tag)).all()
    else:
        images = Image.query.all()

    return jsonify([img.to_dict() for img in images])


@app.route("/images/<int:image_id>", methods=["GET"])
def get_image(image_id):
    """Получить одно изображение по id."""
    image = Image.query.get(image_id)

    if not image:
        return jsonify({"error": "Изображение не найдено"}), 404

    return jsonify(image.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
