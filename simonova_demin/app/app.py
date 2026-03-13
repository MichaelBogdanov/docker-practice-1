from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# SQLite в папке instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/instance/messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# модели данных
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='topic', lazy=True, cascade="all, delete-orphan")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# создание таблиц
with app.app_context():
    # создание папки instance
    os.makedirs('/app/instance', exist_ok=True)
    db.create_all()

# эндпоинты API
@app.route('/topics', methods=['GET', 'POST'])
def handle_topics():
    if request.method == 'GET':
        topics = Topic.query.all()
        return jsonify([{
            'id': t.id,
            'title': t.title,
            'created_at': t.created_at.isoformat() if t.created_at else None,
            'messages_count': len(t.messages)
        } for t in topics])
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        new_topic = Topic(title=data['title'])
        db.session.add(new_topic)
        db.session.commit()
        
        return jsonify({
            'id': new_topic.id,
            'title': new_topic.title,
            'created_at': new_topic.created_at.isoformat() if new_topic.created_at else None
        }), 201

@app.route('/topics/<int:topic_id>/messages', methods=['GET', 'POST'])
def handle_messages(topic_id):
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    if request.method == 'GET':
        messages = Message.query.filter_by(topic_id=topic_id).all()
        return jsonify([{
            'id': m.id,
            'author': m.author,
            'text': m.text,
            'created_at': m.created_at.isoformat() if m.created_at else None
        } for m in messages])
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'author' not in data or 'text' not in data:
            return jsonify({'error': 'Author and text are required'}), 400
        
        new_message = Message(
            topic_id=topic_id,
            author=data['author'],
            text=data['text']
        )
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'id': new_message.id,
            'author': new_message.author,
            'text': new_message.text,
            'created_at': new_message.created_at.isoformat() if new_message.created_at else None
        }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)