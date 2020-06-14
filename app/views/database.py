from werkzeug.exceptions import InternalServerError
from flask import jsonify
from app import db


def is_empty():
    table_names = db.inspect(db.engine).get_table_names()
    is_empty = table_names == []
    return is_empty


def create_all():
    try:
        db.create_all()
        pass
    except Exception:
        raise InternalServerError()


def drop_all():
    try:
        db.drop_all()
        message = 'All tables dropped successfully'
        return jsonify(message=message)
    except Exception:
        raise InternalServerError()
