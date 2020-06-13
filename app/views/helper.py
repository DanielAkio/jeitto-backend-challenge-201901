from werkzeug.exceptions import Unauthorized, NotFound
from werkzeug.security import check_password_hash
from .users import find_by_username
from flask import request, jsonify
from functools import wraps
from app import app
import datetime
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            raise Unauthorized('Missing token key')

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except Exception:
            raise Unauthorized('Token not valid or expired')

        return f(*args, **kwargs)
    return decorated


def token_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            raise Unauthorized('Missing token key')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception:
            raise Unauthorized('Token not valid or expired')

        if data['admin'] is False:
            raise Unauthorized('Token is not a valid admin authentication')

        return f(*args, **kwargs)
    return decorated


def token_yourself_or_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            raise Unauthorized('Missing token key')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception:
            raise Unauthorized('Token not valid or expired')

        if data['admin'] is False and int(data['id']) != int(kwargs.get('id')):
            raise Unauthorized('Only admin can update or delete other users')

        return f(*args, **kwargs)
    return decorated


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        raise Unauthorized('Basic auth="Login Required"')

    user = find_by_username(auth.username)
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
