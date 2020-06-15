from werkzeug.exceptions import Unauthorized, NotFound
from ..views import helper as VHelper, company as VCompany
from flask import jsonify
from app import app


@app.route('/Company', methods=['GET'])
@VHelper.token_admin_required()
def company_find_all():
    companies = VCompany.find()
    if not companies:
        return NotFound('No companies found')
    return jsonify(companies), 200


@app.route('/Company/<company_id>', methods=['GET'])
@VHelper.token_owner_or_admin_required(get_company=True)
def company_find(company, company_id):
    return jsonify(company), 200


@app.route('/Company', methods=['POST'])
@VHelper.token_required(get_user=True)
def company_create(user):
    return VCompany.create(user)


@app.route('/Company/<company_id>', methods=['PUT'])
@VHelper.token_owner_or_admin_required(get_company=True, json_response=False)
def company_edit(company):
    return VCompany.update(company), 200


@app.route('/Company/<company_id>', methods=['DELETE'])
@VHelper.token_required(get_user=True)
def company_logical_delete(user, company_id):
    _company = VCompany.find_by_company_id(company_id, False)
    if (_company.user_id == user['id']) is False:
        return Unauthorized('Only company owners can delete it')
    return VCompany.logical_delete(_company), 200


@app.route('/CompanyRestore/<company_id>', methods=['PUT'])
@VHelper.token_required(get_user=True)
def company_logical_restore(user, company_id):
    _company = VCompany.find_by_company_id(company_id, False)
    if (_company.user_id == user['id']) is False:
        return Unauthorized('Only company owners can delete it')
    return VCompany.logical_restore(_company), 200


@app.route('/CompanyProducts/<int:id>', methods=['POST'])
@VHelper.token_required()
def company_add_product():
    pass


@app.route('/CompanyProducts/<int:id>', methods=['PUT'])
@VHelper.token_required()
def company_edit_product():
    pass


@app.route('/CompanyProducts/<int:id>', methods=['DELETE'])
@VHelper.token_required()
def company_delete_product():
    pass


@app.route('/CompanyProducts', methods=['GET'])
@VHelper.token_required()
def company_list_products():
    pass
