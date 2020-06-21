from werkzeug.exceptions import Conflict, InternalServerError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.product import (
    products_schema as m_products_schema,
    product_schema as m_product_schema,
    Product as m_Product
)
from ..models.company import (
    companies_schema as m_companies_schema,
    company_schema as m_company_schema,
    Company as m_Company
)
from ..models.user import User as m_User
from flask import request
from app import db
import datetime


def find(user: m_User):
    id = request.args.get('company_id')
    if id:
        company = m_Company.query.filter_by(id=id).first()
        if company is None:
            return None
        company_dump = m_company_schema.dump(company)
        products = m_Product.query.filter_by(
            company_id=company_dump['id']
        ).all()
        company_dump['products'] = m_products_schema.dump(products)
        return company_dump
    else:
        companies = m_Company.query.all()
        if companies is None:
            return None
        companies_dump = m_companies_schema.dump(companies)
        for company in companies_dump:
            products = m_Product.query.filter_by(
                company_id=company['id']
            ).all()
            company['products'] = m_products_schema.dump(products)
        return companies_dump


def find_by_id(id: str, json_response=True):
    product = m_Product.query.get(id)
    if json_response:
        return m_product_schema.dump(product)
    return product


def create(product: m_Product):
    try:
        db.session.add(product)
        db.session.commit()
        return m_product_schema.dump(product)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def update(product: m_Product):
    try:
        if 'id' in request.json:
            product.id = request.json['id']
        if 'value' in request.json:
            product.value = request.json['value']
        db.session.commit()
        return m_product_schema.dump(product)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def logical_delete(product: m_Product):
    try:
        product.removed = datetime.datetime.utcnow()
        db.session.commit()
        return m_product_schema.dump(product)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def logical_restore(product: m_Product):
    try:
        product.removed = None
        db.session.commit()
        return m_product_schema.dump(product)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])
