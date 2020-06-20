from ..models import product as m_product
from werkzeug.exceptions import NotFound
from flask import request, jsonify
from ..views import (
    helper as v_helper,
    product as v_product,
    user as v_user
)
from app import app


@app.route('/CompanyProducts', methods=['GET'])
@v_helper.token_required(get_user=True, json_response=True)
def product_find(user):
    products = v_product.find(user)
    if not products:
        return NotFound('No products found')
    return jsonify(products), 200


@app.route('/CompanyProducts/<string:company_id>', methods=['POST'])
@v_helper.request_json_must_have(arguments=['id', 'value'])
@v_helper.token_owner_or_admin_required(get_company=True, json_response=False)
def product_create(company):
    product = m_product.Product(
        request.json['id'], company.company_id, request.json['value']
    )
    return v_product.create(product), 201


@app.route('/CompanyProducts/<id>', methods=['PUT'])
@v_helper.token_required()
def company_edit_product():
    pass


@app.route('/CompanyProducts/<id>', methods=['DELETE'])
@v_helper.token_required()
def company_delete_product():
    pass


@app.route('/CompanyProducts', methods=['GET'])
@v_helper.token_required()
def company_list_products():
    pass
