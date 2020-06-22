from werkzeug.exceptions import NotFound, UnprocessableEntity
from ..models import log as m_log
from flask import request, jsonify
from ..views import (
    product as v_product,
    helper as v_helper,
    log as v_log
)
from app import app


@app.route('/PhoneRecharges', methods=['GET'])
@v_helper.token_required()
def recharge_find():
    id = request.args.get('id')
    phone_number = request.args.get('phone_number')
    if not id and not phone_number:
        message = "Missing id and phone_number into request"
        raise UnprocessableEntity(message)
    log = v_log.find()
    if not log:
        return NotFound('No logs found')
    return jsonify(log), 200


@app.route('/PhoneRecharges', methods=['POST'])
@v_helper.request_json_must_have(arguments=['product_id', 'phone_number'])
@v_helper.token_required(get_user=True, json_response=True)
def recharge(user):
    product = v_product.find_by_id(request.json['product_id'])
    if not product:
        return NotFound('Product not found')
    log = m_log.Log(
        user['id'],
        product['id'],
        product['company_id'],
        request.json['phone_number'],
        product['value']
    )
    return jsonify(v_log.create(log)), 201
