from werkzeug.exceptions import NotFound
from ..views import user, helper
from flask import jsonify
from app import app


@app.route('/User', methods=['GET'])
@helper.token_admin_required()
def user_find_all():
    _users = user.find()
    if not _users:
        return NotFound('No users found')
    return jsonify(_users), 200


@app.route('/User/<id>', methods=['GET'])
@helper.token_yourself_or_admin_required()
def user_find(id):
    _user = user.find_by_id(id)
    if not _user:
        return NotFound('User not found')
    return jsonify(_user), 200


@app.route('/User', methods=['POST'])
def user_create():
    return jsonify(user.create()), 201


@app.route('/User/<id>', methods=['PUT'])
@helper.token_yourself_or_admin_required()
def user_update(id):
    _user = user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(user.update(_user)), 200


@app.route('/User/<id>', methods=['DELETE'])
@helper.token_yourself_or_admin_required()
def user_logical_delete(id):
    _user = user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(user.logical_delete(_user)), 200


@app.route('/UserRestore/<id>', methods=['PUT'])
@helper.token_yourself_or_admin_required()
def user_logical_restore(id):
    _user = user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(user.logical_restore(_user)), 200


@app.route('/UserToAdmin/<id>', methods=['PUT'])
@helper.token_admin_required()
def user_to_admin(id):
    _user = user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(user.to_admin(_user)), 200


@app.route('/UserToCommon/<id>', methods=['PUT'])
@helper.token_admin_required()
def user_to_common(id):
    _user = user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(user.to_common(_user)), 200
