from flask import jsonify
from ..views import users, helper
from app import app


@app.route('/')
@helper.token_required
def root(user):
    return "Hello World"


@app.route('/Auth', methods=['POST'])
def auth():
    try:
        return helper.auth()
    except Exception as e:
        return e


@app.route('/Users', methods=['GET'])
def users_find():
    try:
        return jsonify(users.find()), 200
    except Exception as e:
        return e


@app.route('/Users/<int:id>', methods=['GET'])
def user_find(id):
    try:
        return jsonify(users.find_by_id(id)), 200
    except Exception as e:
        return e


@app.route('/Users', methods=['POST'])
def user_create():
    try:
        return jsonify(users.create()), 201
    except Exception as e:
        return e


@app.route('/Users/<id>', methods=['PUT'])
def user_update(id):
    try:
        user = users.find_by_id(id, False)
        return jsonify(users.update(user)), 200
    except Exception as e:
        return e


@app.route('/Users/<id>', methods=['DELETE'])
def user_delete(id):
    try:
        user = users.find_by_id(id, False)
        return jsonify(users.delete(user)), 200
    except Exception as e:
        return e
