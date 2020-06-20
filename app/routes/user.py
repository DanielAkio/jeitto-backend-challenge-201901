from ..views import user as v_user, helper as v_helper
from werkzeug.exceptions import NotFound
from ..models import user as m_user
from flask import jsonify, request
from app import app


@app.route('/User', methods=['GET'])
@v_helper.token_admin_required()
def user_find_all():
    users = v_user.find()
    if not users:
        return NotFound('No users found')
    return jsonify(users), 200


@app.route('/User/<id>', methods=['GET'])
@v_helper.token_yourself_or_admin_required()
def user_find(id):
    _user = v_user.find_by_id(id)
    if not _user:
        return NotFound('User not found')
    return jsonify(_user), 200


@app.route('/User', methods=['POST'])
@v_helper.request_json_must_have(arguments=['username', 'password'])
def user_create():
    user = m_user.User(request.json['username'], request.json['password'])
    return jsonify(v_user.create(user)), 201


@app.route('/User/<id>', methods=['PUT'])
@v_helper.request_json_must_have(arguments=['username', 'password'])
@v_helper.token_yourself_or_admin_required()
def user_update(id):
    user = v_user.find_by_id(id, json_response=False)
    if not user:
        return NotFound('User not found')
    return jsonify(v_user.update(user)), 200


@app.route('/User/<id>', methods=['DELETE'])
@v_helper.token_yourself_or_admin_required()
def user_logical_delete(id):
    _user = v_user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(v_user.logical_delete(_user)), 200


@app.route('/UserRestore/<id>', methods=['PUT'])
@v_helper.token_yourself_or_admin_required()
def user_logical_restore(id):
    _user = v_user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(v_user.logical_restore(_user)), 200


@app.route('/UserToAdmin/<id>', methods=['PUT'])
@v_helper.token_admin_required()
def user_to_admin(id):
    _user = v_user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(v_user.to_admin(_user)), 200


@app.route('/UserToCommon/<id>', methods=['PUT'])
@v_helper.token_admin_required()
def user_to_common(id):
    _user = v_user.find_by_id(id, json_response=False)
    if not _user:
        return NotFound('User not found')
    return jsonify(v_user.to_common(_user)), 200
