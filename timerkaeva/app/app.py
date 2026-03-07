from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

scores = []

@app.route('/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    
    if not data or 'player' not in data or 'game' not in data or 'score' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_score = {
        "id": str(uuid.uuid4())[:8],
        "player": data['player'],
        "game": data['game'],
        "score": data['score'],
        "date": datetime.now().isoformat()
    }
    
    scores.append(new_score)
    scores.sort(key=lambda x: x['score'], reverse=True)
    
    return jsonify(new_score), 201

@app.route('/scores/top', methods=['GET'])
def get_top():
    game = request.args.get('game')
    limit = request.args.get('limit', default=10, type=int)
    
    if not game:
        return jsonify({"error": "Game parameter is required"}), 400
    
    game_scores = [s for s in scores if s['game'] == game]
    top = game_scores[:limit]
    
    return jsonify(top)

@app.route('/scores/player/<player_name>', methods=['GET'])
def get_player_scores(player_name):
    player_scores = [s for s in scores if s['player'].lower() == player_name.lower()]
    player_scores.sort(key=lambda x: x['date'], reverse=True)
    return jsonify(player_scores)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Scores API is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)