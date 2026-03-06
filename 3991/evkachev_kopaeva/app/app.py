from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

reports = []
report_id = 1

@app.route('/reports', methods=['POST'])
def create_report():
    global report_id
    data = request.get_json()
    
    if not data or 'city' not in data or 'text' not in data or 'temp' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    report = {
        'id': report_id,
        'city': data['city'],
        'text': data['text'],
        'temp': data['temp'],
        'timestamp': datetime.now().isoformat()
    }
    
    reports.append(report)
    report_id += 1
    
    return jsonify(report), 201

@app.route('/reports', methods=['GET'])
def get_reports():
    city = request.args.get('city')
    
    if city:
        filtered_reports = [r for r in reports if r['city'].lower() == city.lower()]
        return jsonify(filtered_reports)
    
    return jsonify(reports)

@app.route('/reports/recent', methods=['GET'])
def get_recent_reports():
    n = request.args.get('n', default=5, type=int)
    
    recent = reports[-n:] if reports else []
    
    return jsonify(list(reversed(recent)))

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)