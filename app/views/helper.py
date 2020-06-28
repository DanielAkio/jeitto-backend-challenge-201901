from werkzeug.exceptions import Unauthorized, NotFound, UnprocessableEntity
from werkzeug.security import check_password_hash
from ..views import user as v_user
from functools import wraps
from flask import request
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

    if check_password_hash(user.password, auth.password):
        expirate_date = datetime.datetime.now() + datetime.timedelta(days=30)
        token = jwt.encode(
            {
                'access': user.access,
                'id': user.id,
                'exp': expirate_date
            }, app.config['SECRET_KEY']
        )
        return {
            'token': token.decode('UTF-8'),
            'expirate_date': str(expirate_date)
        }
    raise Unauthorized('Basic auth="Login Required"')


def _token_required(get_user, json_response, *args, **kwargs):
    token = request.headers.get('x-access-token')
    if not token:
        raise Unauthorized('Missing token key')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except Exception as e:
        raise Unauthorized(f'Jwt decode error: {str(e)}')
    if get_user:
        return v_user.find_by_id(data['id'], json_response)
    return None


def token_required(get_user=False, json_response=False):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            response = _token_required(
                get_user, json_response, *args, **kwargs
            )
            if response:
                kwargs['user'] = response
            return f(*args, **kwargs)
        return function
    return decorator


def _token_admin_required(get_user, *args, **kwargs):
    token = request.headers.get('x-access-token')
    if not token:
        raise Unauthorized('Missing token key')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except Exception as e:
        raise Unauthorized(f'Jwt decode error: {str(e)}')
    if data['access'] != 'admin':
        raise Unauthorized('Token is not a valid admin authentication')
    if get_user:
        return v_user.find_by_id(data['id'], False)
    return None


def token_admin_required(get_user=False):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            response = _token_admin_required(
                get_user, *args, **kwargs
            )
            if response:
                kwargs['user'] = response
            return f(*args, **kwargs)
        return function
    return decorator


def _token_yourself_or_admin_required(get_user, *args, **kwargs):
    token = request.headers.get('x-access-token')
    if not token:
        raise Unauthorized('Missing token key')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except Exception as e:
        raise Unauthorized(f'Jwt decode error: {str(e)}')
    is_admin = data['access'] != 'admin'
    is_yourself = int(data['id']) != int(kwargs.get('id'))
    if is_admin and is_yourself:
        message = 'Permission must be from the admin or yourself'
        raise Unauthorized(message)
    if get_user:
        return v_user.find_by_id(data['id'], False)
    return None


def token_yourself_or_admin_required(get_user=False):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            response = _token_yourself_or_admin_required(
                get_user, *args, **kwargs
            )
            if response:
                kwargs['user'] = response
            return f(*args, **kwargs)
        return function
    return decorator


def _token_owner_or_admin_required(get_user, json_response, *args, **kwargs):
    token = request.headers.get('x-access-token')
    if not token:
        raise Unauthorized('Missing token key')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except Exception as e:
        raise Unauthorized(f'Jwt decode error: {str(e)}')
    if data['access'] == 'common':
        message = 'Permission must be from the admin or owner'
        raise Unauthorized(message)
    if get_user:
        return v_user.find_by_id(data['id'], json_response)
    return None


def token_owner_or_admin_required(get_user=False, json_response=True):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            response = _token_owner_or_admin_required(
                get_user, json_response, *args, **kwargs
            )
            if response:
                kwargs['user'] = response
            return f(*args, **kwargs)
        return function
    return decorator


def _request_json_must_have(arguments, *args, **kwargs):
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


def request_json_must_have(arguments: list):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            _request_json_must_have(arguments, *args, **kwargs)
            return f(*args, **kwargs)
        return function
    return decorator


def _request_json_must_have_one(arguments, *args, **kwargs):
    json = request.json
    message = 'Missing'
    for i, argument in enumerate(arguments):
        message = f'{message} {argument}'
        if (len(arguments) - 1) != i:
            message = f'{message} and'
        else:
            message = f'{message} into request body'
    aux = 0
    arguments_count = len(arguments)
    for argument in arguments:
        if argument not in json:
            aux = aux + 1
    if arguments_count == aux:
        raise UnprocessableEntity(message)


def request_json_must_have_one(arguments: list):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            _request_json_must_have_one(arguments, *args, **kwargs)
            return f(*args, **kwargs)
        return function
    return decorator
