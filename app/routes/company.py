from ..views import helper as v_helper, company as v_company
from werkzeug.exceptions import NotFound
from flask import jsonify
from app import app


@app.route('/Company', methods=['GET'])
@v_helper.token_admin_required()
def company_find_all():
    companies = v_company.find()
    if not companies:
        return NotFound('No companies found')
    return jsonify(companies), 200


@app.route('/Company/<company_id>', methods=['GET'])
@v_helper.token_owner_or_admin_required(get_company=True)
def company_find(company, company_id):
    return jsonify(company), 200


@app.route('/Company', methods=['POST'])
@v_helper.request_json_must_have(arguments=['company_id'])
@v_helper.token_required(get_user=True)
def company_create(user):
    return v_company.create(user), 201


@app.route('/Company/<company_id>', methods=['PUT'])
@v_helper.request_json_must_have(arguments=['company_id', 'user_id'])
@v_helper.token_owner_or_admin_required(get_company=True, json_response=False)
def company_update(company):
    return v_company.update(company), 200


@app.route('/Company/<company_id>', methods=['DELETE'])
@v_helper.token_owner_or_admin_required(get_company=True, json_response=False)
def company_logical_delete(company):
    return v_company.logical_delete(company), 200


@app.route('/CompanyRestore/<string:company_id>', methods=['PUT'])
@v_helper.token_owner_or_admin_required(get_company=True, json_response=False)
def company_logical_restore(company):
    return v_company.logical_restore(company), 200
