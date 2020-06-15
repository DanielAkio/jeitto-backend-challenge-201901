from werkzeug.exceptions import BadRequest
from ..views import user, helper, database
from flask import jsonify
from app import app


@app.route('/DatabaseCreate', methods=['POST'])
def database_create_all():
    if database.is_empty() is False:
        message = 'Before creating, tables must be dropped'
        raise BadRequest(message)
    database.create_all()
    user.create({'username': 'admin', 'password': 'admin'})
    message = 'All tables created successfully'
    accesses = {'login': 'admin', 'password': 'admin'}
    return jsonify(message=message, accesses=accesses), 201


@app.route('/DatabaseDrop', methods=['DELETE'])
@helper.token_admin_required()
def database_drop_all():
    if database.is_empty():
        message = 'The database does not have tables'
        raise BadRequest(message)
    return database.drop_all(), 200
