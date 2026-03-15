from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище заметок в памяти
reports = []


@app.route('/reports', methods=['POST'])
def add_report():
    data = request.get_json()

    # Валидация данных
    if not data or 'city' not in data or 'text' not in data or 'temp' not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_report = {
        "city": data['city'].lower(),
        "text": data['text'],
        "temp": data['temp']
    }
    reports.append(new_report)
    return jsonify(new_report), 201


@app.route('/reports', methods=['GET'])
def get_reports():
    city_filter = request.args.get('city')
    if city_filter:
        filtered = [r for r in reports if r['city'] == city_filter.lower()]
        return jsonify(filtered)
    return jsonify(reports)


@app.route('/reports/recent', methods=['GET'])
def get_recent_reports():
    # Возвращаем последние 5 записей (или все, если их меньше 5)
    return jsonify(reports[-5:])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)