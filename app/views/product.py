from werkzeug.exceptions import Conflict, InternalServerError, Unauthorized
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


def find(user: m_User):
    company_id = request.args.get('company_id')
    if company_id:
        company = m_Company.query.filter_by(
            company_id=company_id
        ).first()
        if company is None:
            return None
        if not user['admin'] and company.user_id != user['id']:
            message = 'User only can see your companies products'
            raise Unauthorized(message)
        company_dump = m_company_schema.dump(company)
        products = m_Product.query.filter_by(
            company_id=company_dump['company_id']
        ).all()
        company_dump['products'] = m_products_schema.dump(products)
        return company_dump
    else:
        if user['admin']:
            companies = m_Company.query.all()
        else:
            companies = m_Company.query.filter_by(user_id=user['id']).all()
        if companies is None:
            return None
        companies_dump = m_companies_schema.dump(companies)
        for company in companies_dump:
            products = m_Product.query.filter_by(
                company_id=company['company_id']
            ).all()
            company['products'] = m_products_schema.dump(products)
        return companies_dump


def create(product: m_Product):
    try:
        db.session.add(product)
        db.session.commit()
        return m_product_schema.dump(product)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])
