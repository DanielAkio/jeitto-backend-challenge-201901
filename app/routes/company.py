from werkzeug.exceptions import Unauthorized
from ..views import helper, company
from app import app


@app.route('/Company', methods=['POST'])
@helper.token_required(True)
def company_create(user):
    return company.create(user)


@app.route('/Company/<company_id>', methods=['PUT'])
@helper.token_required(True)
def company_edit(user, company_id):
    _company = company.find_by_company_id(company_id, False)
    if (_company.user_id == user['id']) is False:
        return Unauthorized('Only company owners can update it')
    return company.update(_company), 200


@app.route('/Company/<company_id>', methods=['DELETE'])
@helper.token_required(True)
def company_logical_delete(user, company_id):
    _company = company.find_by_company_id(company_id, False)
    if (_company.user_id == user['id']) is False:
        return Unauthorized('Only company owners can delete it')
    return company.logical_delete(_company), 200


@app.route('/CompanyRestore/<company_id>', methods=['PUT'])
@helper.token_required(get_user=True)
def company_logical_restore(user, company_id):
    _company = company.find_by_company_id(company_id, False)
    if (_company.user_id == user['id']) is False:
        return Unauthorized('Only company owners can delete it')
    return company.logical_restore(_company), 200


@app.route('/CompanyProducts/<int:id>', methods=['POST'])
@helper.token_required()
def company_add_product():
    pass


@app.route('/CompanyProducts/<int:id>', methods=['PUT'])
@helper.token_required()
def company_edit_product():
    pass


@app.route('/CompanyProducts/<int:id>', methods=['DELETE'])
@helper.token_required()
def company_delete_product():
    pass


@app.route('/CompanyProducts', methods=['GET'])
@helper.token_required()
def company_list_products():
    pass
