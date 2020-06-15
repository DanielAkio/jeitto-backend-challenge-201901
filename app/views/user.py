from werkzeug.exceptions import InternalServerError, BadRequest
from ..models.user import User, user_schema, users_schema
from werkzeug.security import generate_password_hash
from flask import request
from app import db
import datetime


def find_by_id(id, json_response=True):
    user = User.query.get(id)
    if json_response:
        return user_schema.dump(user)
    return user


def find_by_username(username, json_response=True):
    user = User.query.filter_by(username=username, removed=None).first()
    if json_response:
        return user_schema.dump(user)
    return user


def find(json_response=True):
    users = User.query.all()
    if json_response:
        return users_schema.dump(users)
    return users


def create(json=None):
    if json:
        username = json['username']
        password = json['password']
    else:
        try:
            username = request.json['username']
            password = request.json['password']
        except Exception:
            raise BadRequest('Missing json attributes')

    password_hash = generate_password_hash(password)

    if json:
        user = User(username, password_hash, True)
    else:
        user = User(username, password_hash)

    try:
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
    except Exception:
        raise InternalServerError()


def update(user):
    try:
        username = request.json['username']
        password = request.json['password']
    except Exception:
        raise BadRequest('Missing json attributes')

    password_hash = generate_password_hash(password)

    try:
        user.username = username
        user.password = password_hash
        db.session.commit()
        return user_schema.dump(user)
    except Exception:
        raise InternalServerError()


def logical_delete(user):
    try:
        user.removed = datetime.datetime.utcnow()
        db.session.commit()
        return user_schema.dump(user)
    except Exception:
        raise InternalServerError()


def logical_restore(user):
    try:
        user.removed = None
        db.session.commit()
        return user_schema.dump(user)
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
