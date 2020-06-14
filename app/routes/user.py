from ..views import user, helper
from flask import jsonify
from app import app


@app.route('/User', methods=['GET'])
@helper.token_admin_required
def users_find():
    return jsonify(user.find()), 200


@app.route('/User/<int:id>', methods=['GET'])
@helper.token_admin_required
def user_find(id):
    return jsonify(user.find_by_id(id)), 200


@app.route('/User', methods=['POST'])
def user_create():
    return jsonify(user.create()), 201


@app.route('/User/<id>', methods=['PUT'])
@helper.token_yourself_or_admin_required
def user_update(id):
    _user = user.find_by_id(id, False)
    return jsonify(user.update(_user)), 200


@app.route('/User/<id>', methods=['DELETE'])
@helper.token_yourself_or_admin_required
def user_delete(id):
    _user = user.find_by_id(id, False)
    return jsonify(user.delete(_user)), 200


@app.route('/UserToAdmin/<id>', methods=['PUT'])
@helper.token_admin_required
def user_to_admin(id):
    _user = user.find_by_id(id, False)
    return jsonify(user.to_admin(_user)), 200


@app.route('/UserToCommon/<id>', methods=['PUT'])
@helper.token_admin_required
def user_to_common(id):
    _user = user.find_by_id(id, False)
    return jsonify(user.to_common(_user)), 200