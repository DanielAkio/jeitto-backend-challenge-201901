from werkzeug.exceptions import NotFound, InternalServerError, Conflict
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models.user import User as m_User
from ..models.company import (
    companies_schema as m_companies_schema,
    company_schema as m_company_schema,
    Company as m_Company
)
from flask import request
from app import db
import datetime


def find_by_company_id(company_id, json=True):
    company = m_Company.query.filter_by(company_id=company_id).first()
    if company:
        if json:
            return m_company_schema.dump(company)
        return company
    raise NotFound('Company not found')


def find(json=True):
    company = m_Company.query.all()
    if company:
        return m_companies_schema.dump(company)
    raise NotFound('No companies found')


def create(user: m_User):
    company = m_Company(request.json['company_id'], user.id)

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
        company.company_id = request.json['company_id']
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
