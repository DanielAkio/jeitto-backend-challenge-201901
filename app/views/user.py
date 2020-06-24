from werkzeug.exceptions import InternalServerError, Conflict
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.security import generate_password_hash
from ..models.user import (
    User as m_User,
    user_schema as m_user_schema,
    users_schema as m_users_schema
)
from flask import request
from app import db
import datetime


def find():
    users = m_User.query.all()
    return m_users_schema.dump(users)


def find_by_id(id, json_response=True):
    user = m_User.query.get(id)
    if json_response:
        return m_user_schema.dump(user)
    return user


def find_by_username(username, json_response=True):
    user = m_User.query.filter_by(username=username).first()
    if json_response:
        return m_user_schema.dump(user)
    return user


def create(user: m_User):
    try:
        db.session.add(user)
        db.session.commit()
        return m_user_schema.dump(user)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def update(user: m_User):
    try:
        if 'password' in request.json:
            password = request.json['password']
            password_hash = generate_password_hash(password)
            user.password = password_hash
        if 'username' in request.json:
            user.username = request.json['username']
        db.session.commit()
        return m_user_schema.dump(user)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def logical_delete(user: m_User):
    try:
        user.removed = datetime.datetime.utcnow()
        db.session.commit()
        return m_user_schema.dump(user)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def logical_restore(user: m_User):
    try:
        user.removed = None
        db.session.commit()
        return m_user_schema.dump(user)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def access(user: m_User):
    try:
        user.access = request.json['access']
        db.session.commit()
        return m_user_schema.dump(user)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])


def to_common(user):
    try:
        user.access = 'False'
        db.session.commit()
        return m_user_schema.dump(user)
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])
