from flask import Flask, request, jsonify
import json
import random
import os

app = Flask(__name__)

RECIPES_FILE = 'recipes.json'

def load_recipes():
    if os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_recipes(recipes):
    with open(RECIPES_FILE, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

recipes = load_recipes()

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    if not data or 'title' not in data or 'ingredients' not in data or 'steps' not in data:
        return jsonify({'error': 'Missing fields'}), 400
    
    recipe = {
        'id': len(recipes) + 1,
        'title': data['title'],
        'ingredients': [ing.lower() for ing in data['ingredients']],
        'steps': data['steps']
    }
    recipes.append(recipe)
    save_recipes(recipes)
    return jsonify(recipe), 201

@app.route('/recipes', methods=['GET'])
def search_recipes():
    has_param = request.args.get('has', '')
    if not has_param:
        return jsonify(recipes)
    
    required = [ing.strip().lower() for ing in has_param.split(',')]
    result = []
    for recipe in recipes:
        recipe_ings = [ing.lower() for ing in recipe['ingredients']]
        if all(ing in recipe_ings for ing in required):
            result.append(recipe)
    return jsonify(result)

@app.route('/recipes/random', methods=['GET'])
def random_recipe():
    include = request.args.get('include', '')
    if include:
        filtered = [r for r in recipes if include.lower() in [i.lower() for i in r['ingredients']]]
        if not filtered:
            return jsonify({'error': 'No recipes found'}), 404
        return jsonify(random.choice(filtered))
    
    if not recipes:
        return jsonify({'error': 'No recipes'}), 404
    return jsonify(random.choice(recipes))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)