from ..views import helper as v_helper, company as v_company
from werkzeug.exceptions import NotFound, Unauthorized
from ..models import company as m_company
from flask import jsonify, request
from app import app


@app.route('/Company', methods=['GET'])
@v_helper.token_admin_required()
def company_find():
    companies = v_company.find()
    if not companies:
        return NotFound('No companies found')
    return jsonify(companies), 200


@app.route('/Company/<string:id>', methods=['GET'])
@v_helper.token_owner_or_admin_required(get_user=True)
def company_find_by_id(user, id: str):
    company = v_company.find_by_company_id(id)
    if not company:
        return NotFound('Company not found')
    elif company['user_id'] != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can access this data'
        return Unauthorized(message)
    return jsonify(company), 200


@app.route('/Company', methods=['POST'])
@v_helper.request_json_must_have(arguments=['id'])
@v_helper.token_owner_or_admin_required(get_user=True)
def company_create(user):
    company = m_company.Company(request.json['id'], user['id'])
    return v_company.create(company), 201


@app.route('/Company/<string:id>', methods=['PUT'])
@v_helper.request_json_must_have_one(arguments=['id', 'user_id'])
@v_helper.token_owner_or_admin_required(get_user=True)
def company_update(user, id: str):
    company = v_company.find_by_company_id(id, json_response=False)
    if not company:
        return NotFound('Company not found')
    elif company.user_id != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can access this data'
        return Unauthorized(message)
    return v_company.update(company), 200


@app.route('/Company/<string:id>', methods=['DELETE'])
@v_helper.token_owner_or_admin_required(get_user=True)
def company_logical_delete(user, id: str):
    company = v_company.find_by_company_id(id, json_response=False)
    if not company:
        return NotFound('Company not found')
    elif company.user_id != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can access this data'
        return Unauthorized(message)
    return v_company.logical_delete(company), 200


@app.route('/CompanyRestore/<string:id>', methods=['PUT'])
@v_helper.token_owner_or_admin_required(get_user=True)
def company_logical_restore(user, id: str):
    company = v_company.find_by_company_id(id, json_response=False)
    if not company:
        return NotFound('Company not found')
    elif company.user_id != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can access this data'
        return Unauthorized(message)
    return v_company.logical_restore(company), 200
