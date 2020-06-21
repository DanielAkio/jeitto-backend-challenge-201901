from werkzeug.exceptions import NotFound, Unauthorized
from ..models import product as m_product
from flask import request, jsonify
from ..views import (
    product as v_product,
    company as v_company,
    helper as v_helper
)
from app import app


@app.route('/CompanyProducts', methods=['GET'])
@v_helper.token_required(get_user=True, json_response=True)
def product_find(user):
    products = v_product.find(user)
    if not products:
        return NotFound('No products found')
    return jsonify(products), 200


@app.route('/CompanyProducts/<string:id>', methods=['POST'])
@v_helper.request_json_must_have(arguments=['id', 'value'])
@v_helper.token_owner_or_admin_required(get_user=True, json_response=True)
def product_create(user, id):
    company = v_company.find_by_company_id(id, json_response=False)
    if not company:
        return NotFound('Company not found')
    elif company.user_id != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can create a product'
        return Unauthorized(message)
    product = m_product.Product(
        request.json['id'], company.id, request.json['value']
    )
    return v_product.create(product), 201


@app.route('/CompanyProducts/<string:id>', methods=['PUT'])
@v_helper.request_json_must_have_one(arguments=['id', 'value'])
@v_helper.token_owner_or_admin_required(get_user=True, json_response=True)
def product_update(user, id):
    product = v_product.find_by_id(id, json_response=False)
    if not product:
        return NotFound('Product not found')
    company = v_company.find_by_company_id(
        product.company_id, json_response=False
    )
    if not company:
        return NotFound('Company not found')
    elif company.user_id != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can update a product'
        return Unauthorized(message)
    return jsonify(v_product.update(product)), 200


@app.route('/CompanyProducts/<string:id>', methods=['DELETE'])
@v_helper.token_owner_or_admin_required(get_user=True, json_response=True)
def product_logical_delete(user, id):
    product = v_product.find_by_id(id, json_response=False)
    if not product:
        return NotFound('Product not found')
    company = v_company.find_by_company_id(
        product.company_id, json_response=False
    )
    if not company:
        return NotFound('Company not found')
    elif company.user_id != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can update a product'
        return Unauthorized(message)
    return jsonify(v_product.logical_delete(product)), 200


@app.route('/CompanyProductsRestore/<string:id>', methods=['PUT'])
@v_helper.token_owner_or_admin_required(get_user=True, json_response=True)
def product_logical_restore(user, id):
    product = v_product.find_by_id(id, json_response=False)
    if not product:
        return NotFound('Product not found')
    company = v_company.find_by_company_id(
        product.company_id, json_response=False
    )
    if not company:
        return NotFound('Company not found')
    elif company.user_id != user['id'] and user['access'] != 'admin':
        message = 'Only the owner of the company or admin can update a product'
        return Unauthorized(message)
    return jsonify(v_product.logical_restore(product)), 200
