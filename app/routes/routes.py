from ..views import user, helper, database
from flask import jsonify
from app import app


@app.route('/DatabaseCreate', methods=['POST'])
def create_all():
    if database.is_empty() is False:
        message = 'Before creating, tables must be dropped'
        return jsonify(message=message), 400
    database.create_all()
    user.create({'username': 'admin', 'password': 'admin'})
    message = 'All tables created successfully'
    accesses = {'login': 'admin', 'password': 'admin'}
    return jsonify(message=message, accesses=accesses), 201


@app.route('/DatabaseDrop', methods=['DELETE'])
@helper.token_admin_required
def drop_all():
    return database.drop_all(), 200


@app.route('/Auth', methods=['POST'])
def auth():
    return helper.auth()


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
