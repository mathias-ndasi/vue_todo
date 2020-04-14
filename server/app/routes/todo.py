from flask import jsonify, Blueprint, request
from marshmallow.exceptions import ValidationError

from app import models, db
from app.utils import util
from app.schemas import schema_todo
from app.auth import decorators

todo = Blueprint('todo', __name__, url_prefix='/account')


@todo.route('/<string:public_id>/todo', methods=['POST'])
@decorators.token_required
def create_todo(public_id):
    error = None
    message = None
    success = False
    results = None

    data = request.get_json()

    if not data:
        error = {'title': 'Json data is required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    try:
        clean_data = schema_todo.todo_schema.load(data)

        user = models.User.query.filter_by(
            public_id=public_id, active=True).first()

        if not user:
            error = {'title': 'User not found'}
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        new_todo = models.Todo(
            title=clean_data['title'], created_by=user.public_id)
        db.session.add(new_todo)
        db.session.commit()

        success = True
        message = 'Todo created successfully'
        results = schema_todo.todo_schema.dump(new_todo)

        return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('CREATED')

    except ValidationError as e:
        error = e.normalized_messages()

    return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')


@todo.route('/<string:public_id>/todo', methods=['GET'])
@decorators.token_required
def get_all_user_todos(public_id):
    error = None
    message = None
    success = False
    results = None

    if not public_id:
        error = {'general': 'user public_id is required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user = models.User.query.filter_by(
        public_id=public_id, active=True).first()

    if not user:
        error = {'general': 'Invalid public_id'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    todos = user.todos

    if len(todos) == 0:
        message = 'No Todo Available'

    results = schema_todo.todo_schemas.dump(todos)
    success = True

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')


@todo.route('/<string:public_id>/todo/<int:todo_id>', methods=['GET'])
@decorators.token_required
def get_single_user_todos(public_id, todo_id):
    error = None
    message = None
    success = False
    results = None

    if not public_id and not todo_id:
        error = {'general': 'user public_id and todo_id are required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user = models.User.query.filter_by(
        public_id=public_id, active=True).first()

    if not user:
        error = {'general': 'Invalid public_id'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    todo = models.Todo.query.filter_by(
        id=todo_id, created_by=user.public_id).first()

    if not todo:
        error = {'general': 'Todo not found'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    results = schema_todo.todo_schema.dump(todo)
    success = True

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')


@todo.route('/<string:public_id>/todo/<int:todo_id>/done', methods=['PUT'])
@decorators.token_required
def toggle_todo_done(public_id, todo_id):
    error = None
    message = None
    success = False
    results = None

    if not public_id and not todo_id:
        error = {'general': 'user public_id and todo_id are required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user = models.User.query.filter_by(
        public_id=public_id, active=True).first()

    if not user:
        error = {'general': 'Invalid public_id'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    todo = models.Todo.query.filter_by(
        id=todo_id, created_by=user.public_id).first()

    if not todo:
        error = {'general': 'Todo not found'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    if todo.done:
        todo.done = False
    else:
        todo.done = True

    db.session.commit()
    results = schema_todo.todo_schema.dump(todo)
    success = True

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')


@todo.route('/<string:public_id>/todo/<int:todo_id>', methods=['PUT'])
@decorators.token_required
def update_todo(public_id, todo_id):
    error = None
    message = None
    success = False
    results = None

    if not public_id and not todo_id:
        error = {'general': 'user public_id and todo_id are required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user = models.User.query.filter_by(
        public_id=public_id, active=True).first()

    if not user:
        error = {'general': 'Invalid public_id'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    todo = models.Todo.query.filter_by(
        id=todo_id, created_by=user.public_id).first()

    if not todo:
        error = {'general': 'Todo not found'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    data = request.get_json()

    if not data:
        error = {'title': 'Json data is required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    try:
        clean_data = schema_todo.todo_schema.load(data)
        todo.title = clean_data.get('title', todo.title)

        db.session.commit()
        results = schema_todo.todo_schema.dump(todo)
        success = True
        message = "Update was successful"

        return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')

    except ValidationError as e:
        error = e.normalized_messages()
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')


@todo.route('/<string:public_id>/todo/<int:todo_id>', methods=['DELETE'])
@decorators.token_required
def delete_todo(public_id, todo_id):
    error = None
    message = None
    success = False
    results = None

    if not public_id and not todo_id:
        error = {'general': 'user public_id and todo_id are required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user = models.User.query.filter_by(
        public_id=public_id, active=True).first()

    if not user:
        error = {'general': 'Invalid public_id'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    todo = models.Todo.query.filter_by(
        id=todo_id, created_by=user.public_id).first()

    if not todo:
        error = {'general': 'Todo not found'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    db.session.delete(todo)
    db.session.commit()
    success = True
    message = "Todo deleted successfully!!!"

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('NO_CONTENT')
