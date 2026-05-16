# трекер привычек на Flask
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

habits = []
next_id = 1


@app.route('/habits', methods=['GET'])
def get_habits():
    return jsonify(habits)


@app.route('/habits', methods=['POST'])
def create_habit():
    global next_id
    data = request.get_json()
    habit = {
        'id': next_id,
        'name': data.get('name', ''),
        'user_id': data.get('user_id', 0),
        'checks': []
    }
    habits.append(habit)
    next_id += 1
    return jsonify(habit), 201


@app.route('/habits/<int:habit_id>/check', methods=['POST'])
def check_habit(habit_id):
    data = request.get_json()
    date_str = data.get('date', '')
    for h in habits:
        if h['id'] == habit_id:
            h['checks'].append(date_str)
            return jsonify(h)
    return jsonify({'error': 'not found'}), 404


@app.route('/habits/<int:habit_id>/streak', methods=['GET'])
def get_streak(habit_id):
    for h in habits:
        if h['id'] == habit_id:
            if not h['checks']:
                return jsonify({'streak': 0})
            dates = sorted(h['checks'])
            streak = 1
            last = datetime.strptime(dates[-1], '%Y-%m-%d').date()
            for i in range(len(dates) - 2, -1, -1):
                curr = datetime.strptime(dates[i], '%Y-%m-%d').date()
                if (last - curr).days == streak:
                    streak += 1
                else:
                    break
            return jsonify({'streak': streak})
    return jsonify({'error': 'not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
