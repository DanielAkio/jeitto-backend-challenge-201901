from werkzeug.exceptions import Unauthorized, NotFound
from werkzeug.security import check_password_hash
from .users import user_by_username
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
            return Unauthorized('Missing token key')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_by_username(username=data['username'])
        except Exception:
            return Unauthorized('Token not valid or expired')

        return f(current_user, *args, **kwargs)
    return decorated


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        raise Unauthorized('Basic auth="Login Required"')

    user = user_by_username(auth.username)
    if not user:
        raise NotFound('User not found')

    if user and check_password_hash(user.password, auth.password):
        expirate_date = datetime.datetime.now() + datetime.timedelta(days=1)
        token = jwt.encode(
            {'username': user.username, 'exp': expirate_date},
            app.config['SECRET_KEY']
        )
        return jsonify({
            'token': token.decode('UTF-8'), 'expirate_date': expirate_date
        })

    raise Unauthorized('Basic auth="Login Required"')
