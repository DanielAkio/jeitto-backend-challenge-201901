from werkzeug.exceptions import InternalServerError, Conflict
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models.company import (
    companies_schema as m_companies_schema,
    company_schema as m_company_schema,
    Company as m_Company
)
from flask import request
from app import db
import datetime


def find():
    company = m_Company.query.all()
    return m_companies_schema.dump(company)


def find_by_company_id(id, json_response=True):
    company = m_Company.query.get(id)
    if json_response:
        return m_company_schema.dump(company)
    return company


def create(company: m_Company):
    try:
        db.session.add(company)
        db.session.commit()
        return m_company_schema.dump(company)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def update(company: m_Company):
    try:
        if 'id' in request.json:
            company.id = request.json['id']
        if 'user_id' in request.json:
            company.user_id = request.json['user_id']
        db.session.commit()
        return m_company_schema.dump(company)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def logical_delete(company):
    try:
        company.removed = datetime.datetime.utcnow()
        db.session.commit()
        return m_company_schema.dump(company)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def logical_restore(company):
    try:
        company.removed = None
        db.session.commit()
        return m_company_schema.dump(company)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])
