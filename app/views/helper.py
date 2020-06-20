from werkzeug.exceptions import Unauthorized, NotFound, UnprocessableEntity
from ..views import user as v_user, company as v_company
from werkzeug.security import check_password_hash
from ..models import company as m_company
from flask import request, jsonify
from functools import wraps
from app import app
import datetime
import jwt


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        raise Unauthorized('Basic auth="Login Required"')
    user = v_user.find_by_username(auth.username, json_response=False)
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


def token_required(get_user=False, json_response=False):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            token = request.headers.get('x-access-token')
            if not token:
                raise Unauthorized('Missing token key')

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except jwt.exceptions.DecodeError as e:
                raise Unauthorized(f'Jwt decode error: {str(e)}')

            if get_user:
                kwargs['user'] = v_user.find_by_id(data['id'], json_response)
                return f(*args, **kwargs)
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
            except jwt.exceptions.DecodeError as e:
                raise Unauthorized(f'Jwt decode error: {str(e)}')

            if data['admin'] is False:
                raise Unauthorized('Token is not a valid admin authentication')

            if get_user:
                user = v_user.find_by_id(data['id'], False)
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
            except jwt.exceptions.DecodeError as e:
                raise Unauthorized(f'Jwt decode error: {str(e)}')

            is_admin = data['admin'] is False
            is_yourself = int(data['id']) != int(kwargs.get('id'))
            if is_admin and is_yourself:
                message = 'Permission must be from the admin or yourself'
                raise Unauthorized(message)
            if get_user:
                user = v_user.find_by_id(data['id'], False)
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
            except jwt.exceptions.DecodeError as e:
                raise Unauthorized(f'Jwt decode error: {str(e)}')

            company = v_company.find_by_company_id(
                kwargs.get('company_id'), False
            )
            if not company:
                raise NotFound('Company not found')
            if data['admin'] is False and int(data['id']) != company.user_id:
                message = 'Permission must be from the admin or owner'
                raise Unauthorized(message)
            if get_company:
                del kwargs['company_id']
                if json_response:
                    kwargs['company'] = (
                        m_company.company_schema.dump(company)
                    )
                    return f(*args, **kwargs)
                kwargs['company'] = company
                return f(*args, **kwargs)
            return f(*args, **kwargs)
        return function
    return decorator


def request_json_must_have(arguments: list):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            json = request.json
            message = 'Missing'
            for i, argument in enumerate(arguments):
                message = f'{message} {argument}'
                if (len(arguments) - 1) != i:
                    message = f'{message} or'
                else:
                    message = f'{message} into request body'
            for argument in arguments:
                if argument not in json:
                    raise UnprocessableEntity(message)
            return f(*args, **kwargs)
        return function
    return decorator
