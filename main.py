from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import DB_USERNAME, DB_PASSWORD, DB_NAME

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5433/{DB_NAME}'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Task model
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50))

    def __init__(self, title, description, priority, due_date, category=None, completed=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.completed = completed

# for serialization/deserialization
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'completed', 'priority', 'due_date', 'category')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# Endpoint to test
@app.route('/test', methods=['GET'])
def test_1():
    return 'Hello Youssef!'

# Endpoint to retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# Endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if 'title' not in request.json:
        error_message = 'Title is required'
        response = make_response(jsonify({'error': error_message}), 400)
        response.headers['Content-Type'] = 'text/plain'
        abort(response)
    if 'description' not in request.json:
        error_message = 'Description is required'
        response = make_response(jsonify({'error': error_message}), 400)
        response.headers['Content-Type'] = 'text/plain'
        abort(response)
    title = request.json['title']
    description = request.json['description']
    priority = request.json.get('priority')
    due_date = request.json.get('due_date')
    category = request.json.get('category')
    completed = request.json.get('completed')
    new_task = Task(title, description, priority, due_date, category, completed)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# Endpoint to retrieve a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return task_schema.jsonify(task)
    return jsonify({'message': 'Task not found'})

# Endpoint to update a specific task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        if 'title' in request.json:
            task.title = request.json['title']
        if 'description' in request.json:
            task.description = request.json['description']
        if 'priority' in request.json:
            task.priority = request.json['priority']
        if 'due_date' in request.json:
            task.due_date = request.json['due_date']
        if 'category' in request.json:
            task.category = request.json['category']
        if 'completed' in request.json:
            task.completed = request.json['completed']
        db.session.commit()
        return task_schema.jsonify(task)
    return jsonify({'message': 'Task not found'})

# Endpoint to delete a specific task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'message': 'Task not found'})

if __name__ == '__main__':
    app.run(debug=True)
