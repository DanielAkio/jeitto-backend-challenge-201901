from werkzeug.exceptions import NotFound, InternalServerError, BadRequest
from ..models.company import Company, company_schema, companies_schema
from flask import request
from app import db
import datetime


def find_by_company_id(company_id, json=True):
    company = Company.query.get(company_id)
    if company:
        if json:
            return company_schema.dump(company)
        return company
    raise NotFound('Company not found')


def find(json=True):
    company = Company.query.all()
    if company:
        return companies_schema.dump(company)
    raise NotFound('No companies found')


def create(user):
    try:
        company_id = request.json['company_id']
    except Exception:
        raise BadRequest('Missing json attributes')

    company = Company(company_id, user.id)

    try:
        db.session.add(company)
        db.session.commit()
        return company_schema.dump(company)
    except Exception:
        raise InternalServerError()


def update(company):
    try:
        user_id = request.json['user_id']
    except Exception:
        raise BadRequest('Missing json attributes')

    try:
        company.user_id = user_id
        db.session.commit()
        return company_schema.dump(company)
    except Exception:
        raise InternalServerError()


def logical_delete(company):
    try:
        company.removed = datetime.datetime.utcnow()
        db.session.commit()
        return company_schema.dump(company)
    except Exception:
        raise InternalServerError()


def logical_restore(company):
    try:
        company.removed = None
        db.session.commit()
        return company_schema.dump(company)
    except Exception:
        raise InternalServerError()


def to_admin(user):
    try:
        user.admin = True
        db.session.commit()
        return user_schema.dump(user)
    except Exception:
        return InternalServerError()


def to_common(user):
    try:
        user.admin = False
        db.session.commit()
        return user_schema.dump(user)
    except Exception:
        return InternalServerError()
