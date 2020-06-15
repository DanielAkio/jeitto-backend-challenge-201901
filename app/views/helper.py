from werkzeug.exceptions import Unauthorized, NotFound
from werkzeug.security import check_password_hash
from .user import find_by_username, find_by_id
from .company import find_by_company_id
from flask import request, jsonify
from ..models import company
from functools import wraps
from app import app
import datetime
import jwt


def token_required(get_user=False):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            token = request.headers.get('x-access-token')

            if not token:
                raise Unauthorized('Missing token key')

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except Exception:
                raise Unauthorized('Token not valid or expired')

            if get_user:
                user = find_by_id(data['id'], False)
                return f(user, *args, **kwargs)
            return f(*args, **kwargs)
        return function
    return decorator


def token_admin_required(get_user=False):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            token = request.headers.get('x-access-token')
            if not token:
                raise Unauthorized('Missing token key')

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except Exception:
                raise Unauthorized('Token not valid or expired')

            if data['admin'] is False:
                raise Unauthorized('Token is not a valid admin authentication')

            if get_user:
                user = find_by_id(data['id'], False)
                return f(user, *args, **kwargs)
            return f(*args, **kwargs)
        return function
    return decorator


def token_yourself_or_admin_required(get_user=False):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            token = request.headers.get('x-access-token')
            if not token:
                raise Unauthorized('Missing token key')

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except Exception:
                raise Unauthorized('Token not valid or expired')

            is_admin = data['admin'] is False
            is_yourself = int(data['id']) != int(kwargs.get('id'))
            if is_admin and is_yourself:
                message = 'Permission must be from the admin or yourself'
                raise Unauthorized(message)

            if get_user:
                user = find_by_id(data['id'], False)
                return f(user, *args, **kwargs)
            return f(*args, **kwargs)
        return function
    return decorator


def token_owner_or_admin_required(get_company=False, json_response=True):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            token = request.headers.get('x-access-token')
            if not token:
                raise Unauthorized('Missing token key')

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except Exception:
                raise Unauthorized('Token not valid or expired')

            _company = find_by_company_id(kwargs.get('company_id'), False)
            if not _company:
                raise NotFound('Company not found')

            is_admin = data['admin'] is False
            is_owner = int(data['id']) != _company.user_id
            if is_admin and is_owner:
                message = 'Permission must be from the admin or owner'
                raise Unauthorized(message)

            if get_company:
                if json_response:
                    _company = company.company_schema.dump(_company)
                    return f(_company, *args, **kwargs)
                return f(_company, *args, **kwargs)
            return f(*args, **kwargs)
        return function
    return decorator


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        raise Unauthorized('Basic auth="Login Required"')

    user = find_by_username(auth.username, json_response=False)
    if not user:
        raise NotFound('User not found')

    if user and check_password_hash(user.password, auth.password):
        expirate_date = datetime.datetime.now() + datetime.timedelta(days=1)
        token = jwt.encode(
            {
                'admin': user.admin,
                'id': user.id,
                'exp': expirate_date
            }, app.config['SECRET_KEY']
        )
        return jsonify({
            'token': token.decode('UTF-8'), 'expirate_date': expirate_date
        })

    raise Unauthorized('Basic auth="Login Required"')
