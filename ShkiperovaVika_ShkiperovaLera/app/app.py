from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

tasks = []
next_id = 1

@app.route('/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    priority = request.args.get('priority')

    filtered = tasks
    if status:
        filtered = [t for t in filtered if t.get("status") == status]
    if priority:
        filtered = [t for t in filtered if str(t.get("priority")) == str(priority)]

    return jsonify(filtered), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()

    if not data or "title" not in data or "due" not in data or "priority" not in data:
        return jsonify({"error": "Invalid input"}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "due": data["due"],
        "priority": data["priority"],
        "status": "open"
    }
    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.get_json()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if "status" in data:
        task["status"] = data["status"]

    return jsonify(task), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
