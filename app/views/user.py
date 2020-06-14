from werkzeug.exceptions import NotFound, InternalServerError, BadRequest
from ..models.user import User, user_schema, users_schema
from werkzeug.security import generate_password_hash
from flask import request
from app import db


def find_by_id(id, json=True):
    user = User.query.get(id)
    if user:
        if json:
            return user_schema.dump(user)
        return user
    raise NotFound('User not found')


def find_by_username(username):
    user = User.query.filter(User.username == username).one()
    if user:
        return user
    return NotFound('User not found')


def find(json=True):
    users = User.query.all()
    if users:
        return users_schema.dump(users)
    raise NotFound('No users found')


def create(json=None):
    if json:
        username = json['username']
        password = json['password']
    else:
        try:
            username = request.json['username']
            password = request.json['password']
        except Exception:
            raise BadRequest()

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
        raise BadRequest()

    password_hash = generate_password_hash(password)

    try:
        user.username = username
        user.password = password_hash
        db.session.commit()
        return user_schema.dump(user)
    except Exception:
        raise InternalServerError()


def delete(user):
    try:
        db.session.delete(user)
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
