from ..views import user as v_user, helper as v_helper, database as v_database
from werkzeug.exceptions import BadRequest
from ..models import user as m_user
from flask import jsonify
from app import app


@app.route('/DatabaseCreate', methods=['POST'])
def database_create_all():
    if v_database.is_empty() is False:
        message = 'Before creating, tables must be dropped'
        raise BadRequest(message)
    v_database.create_all()
    v_user.create(m_user.User('admin', 'admin', True))
    message = 'All tables created successfully'
    accesses = {'login': 'admin', 'password': 'admin'}
    return jsonify(message=message, accesses=accesses), 201


@app.route('/DatabaseDrop', methods=['DELETE'])
@v_helper.token_admin_required()
def database_drop_all():
    if v_database.is_empty():
        message = 'The database does not have tables'
        raise BadRequest(message)
    v_database.drop_all()
    message = 'All tables dropped successfully'
    return jsonify(message=message), 200
