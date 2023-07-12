from flask import Flask, jsonify, request
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
    title = request.json['title']
    description = request.json['description']
    priority = request.json['priority']
    due_date = request.json['due_date']
    category = request.json.get('category')
    new_task = Task(title, description, priority, due_date, category)
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
        task.title = request.json['title']
        task.description = request.json['description']
        task.priority = request.json['priority']
        task.due_date = request.json['due_date']
        task.category = request.json.get('category')
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
