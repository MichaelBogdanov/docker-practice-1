import random
from flask import Flask, request, jsonify

app = Flask(__name__)

recipes = []
next_id = 1


def normalize_ingredient(value):
    return str(value).strip().lower()


@app.route("/recipes", methods=["POST"])
def create_recipe():
    global next_id

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    required_fields = ["title", "ingredients", "steps"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    title = str(data["title"]).strip()
    ingredients = data["ingredients"]
    steps = str(data["steps"]).strip()

    if not title:
        return jsonify({"error": "title is empty"}), 400

    if not isinstance(ingredients, list) or len(ingredients) == 0:
        return jsonify({"error": "ingredients must be a non-empty list"}), 400

    if not steps:
        return jsonify({"error": "steps is empty"}), 400

    clean_ingredients = [
        normalize_ingredient(ingredient)
        for ingredient in ingredients
        if str(ingredient).strip()
    ]

    if len(clean_ingredients) == 0:
        return jsonify({"error": "ingredients list is empty"}), 400

    recipe = {
        "id": next_id,
        "title": title,
        "ingredients": clean_ingredients,
        "steps": steps
    }

    recipes.append(recipe)
    next_id += 1

    return jsonify(recipe), 201


@app.route("/recipes", methods=["GET"])
def get_recipes():
    has_param = request.args.get("has")

    if not has_param:
        return jsonify(recipes), 200

    required_ingredients = [
        normalize_ingredient(item)
        for item in has_param.split(",")
        if item.strip()
    ]

    filtered_recipes = []
    for recipe in recipes:
        recipe_ingredients = set(recipe["ingredients"])
        if all(ingredient in recipe_ingredients for ingredient in required_ingredients):
            filtered_recipes.append(recipe)

    return jsonify(filtered_recipes), 200


@app.route("/recipes/random", methods=["GET"])
def get_random_recipe():
    include = request.args.get("include")

    if include:
        include_ingredient = normalize_ingredient(include)
        filtered = [
            recipe
            for recipe in recipes
            if include_ingredient in recipe["ingredients"]
        ]
    else:
        filtered = recipes

    if not filtered:
        return jsonify({"error": "no recipes found"}), 404

    return jsonify(random.choice(filtered)), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Recipes API running",
        "endpoints": {
            "POST /recipes": "create recipe",
            "GET /recipes": "list recipes or filter by ingredients",
            "GET /recipes?has=egg,milk": "find recipes containing all listed ingredients",
            "GET /recipes/random": "get random recipe",
            "GET /recipes/random?include=tomato": "get random recipe with ingredient"
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
