from ..views import users, helper
from flask import jsonify
from app import app


@app.route('/Auth', methods=['POST'])
def auth():
    return helper.auth()


@app.route('/User', methods=['GET'])
@helper.token_admin_required
def users_find():
    return jsonify(users.find()), 200


@app.route('/User/<int:id>', methods=['GET'])
@helper.token_admin_required
def user_find(id):
    return jsonify(users.find_by_id(id)), 200


@app.route('/User', methods=['POST'])
def user_create():
    return jsonify(users.create()), 201


@app.route('/User/<id>', methods=['PUT'])
@helper.token_yourself_or_admin_required
def user_update(id):
    user = users.find_by_id(id, False)
    return jsonify(users.update(user)), 200


@app.route('/User/<id>', methods=['DELETE'])
@helper.token_yourself_or_admin_required
def user_delete(id):
    user = users.find_by_id(id, False)
    return jsonify(users.delete(user)), 200


@app.route('/UserToAdmin/<id>', methods=['PUT'])
@helper.token_admin_required
def user_to_admin(id):
    user = users.find_by_id(id, False)
    return jsonify(users.to_admin(user)), 200


@app.route('/UserToCommon/<id>', methods=['PUT'])
@helper.token_admin_required
def user_to_common(id):
    user = users.find_by_id(id, False)
    return jsonify(users.to_common(user)), 200
