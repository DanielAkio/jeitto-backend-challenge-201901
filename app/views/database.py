from werkzeug.exceptions import InternalServerError
from app import db


def is_empty():
    table_names = db.inspect(db.engine).get_table_names()
    is_empty = table_names == []
    return is_empty


def create_all():
    try:
        db.create_all()
        pass
    except Exception as e:
        raise InternalServerError(str(e))


def drop_all():
    try:
        db.drop_all()
        pass
    except Exception as e:
        raise InternalServerError(str(e))
