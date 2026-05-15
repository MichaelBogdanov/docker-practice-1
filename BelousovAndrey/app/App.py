from flask import Flask, request, jsonify
import random

app = Flask(__name__)
recipes = []
next_id = 1

@app.route('/recipes', methods=['GET'])
def get_recipes():
    has = request.args.get('has')
    result = recipes
    if has:
        ingredients = set(i.strip().lower() for i in has.split(','))
        result = [r for r in recipes if ingredients.issubset(set(ing.lower() for ing in r['ingredients']))]
    return jsonify(result)

@app.route('/recipes/random', methods=['GET'])
def get_random_recipe():
    include = request.args.get('include', '').lower()
    pool = [r for r in recipes if include in [i.lower() for i in r['ingredients']]] if include else recipes
    return jsonify(random.choice(pool) if pool else {})

@app.route('/recipes', methods=['POST'])
def add_recipe():
    global next_id
    data = request.get_json()
    recipe = {
        'id': next_id,
        'title': data['title'],
        'ingredients': data['ingredients'],
        'steps': data.get('steps', '')
    }
    recipes.append(recipe)
    next_id += 1
    return jsonify(recipe), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
