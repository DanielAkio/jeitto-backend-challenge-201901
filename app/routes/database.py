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
