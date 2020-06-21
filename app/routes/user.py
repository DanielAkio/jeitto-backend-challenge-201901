from werkzeug.exceptions import NotFound, UnprocessableEntity
from ..views import user as v_user, helper as v_helper
from ..models import user as m_user
from flask import jsonify, request
from app import app


@app.route('/User', methods=['GET'])
@v_helper.token_admin_required()
def user_find():
    users = v_user.find()
    if not users:
        return NotFound('No users found')
    return jsonify(users), 200


@app.route('/User/<id>', methods=['GET'])
@v_helper.token_yourself_or_admin_required()
def user_find_by_id(id):
    user = v_user.find_by_id(id)
    if not user:
        return NotFound('User not found')
    return jsonify(user), 200


@app.route('/User', methods=['POST'])
@v_helper.request_json_must_have(arguments=['username', 'password'])
def user_create():
    user = m_user.User(request.json['username'], request.json['password'])
    return jsonify(v_user.create(user)), 201


@app.route('/User/<id>', methods=['PUT'])
@v_helper.request_json_must_have_one(arguments=['username', 'password'])
@v_helper.token_yourself_or_admin_required()
def user_update(id):
    user = v_user.find_by_id(id, json_response=False)
    if not user:
        return NotFound('User not found')
    return jsonify(v_user.update(user)), 200


@app.route('/User/<id>', methods=['DELETE'])
@v_helper.token_yourself_or_admin_required()
def user_logical_delete(id):
    user = v_user.find_by_id(id, json_response=False)
    if not user:
        return NotFound('User not found')
    return jsonify(v_user.logical_delete(user)), 200


@app.route('/UserRestore/<id>', methods=['PUT'])
@v_helper.token_yourself_or_admin_required()
def user_logical_restore(id):
    user = v_user.find_by_id(id, json_response=False)
    if not user:
        return NotFound('User not found')
    return jsonify(v_user.logical_restore(user)), 200


@app.route('/UserAccess/<id>', methods=['PUT'])
@v_helper.request_json_must_have(arguments=['access'])
@v_helper.token_admin_required()
def user_access(id):
    if request.json['access'] not in ['admin', 'owner', 'common']:
        message = 'Access must be: admin, owner or common'
        raise UnprocessableEntity(message)
    user = v_user.find_by_id(id, json_response=False)
    if not user:
        return NotFound('User not found')
    return jsonify(v_user.access(user)), 200
