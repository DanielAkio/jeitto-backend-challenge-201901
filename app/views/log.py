from werkzeug.exceptions import Conflict, InternalServerError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models.log import (
    logs_schema as m_logs_schema,
    log_schema as m_log_schema,
    Log as m_Log
)
from flask import request
from app import db


def find():
    id = request.args.get('id')
    if id:
        log = m_Log.query.get(id)
        if not log:
            return None
        return m_log_schema.dump(log)
    else:
        logs = m_Log.query.filter_by(
            phone_number=request.args.get('phone_number')
        ).all()
        if not logs:
            return None
        return m_logs_schema.dump(logs)


def create(log: m_Log):
    try:
        db.session.add(log)
        db.session.commit()
        return m_log_schema.dump(log)
    except IntegrityError as e:
        raise Conflict(e.orig.args[1])
    except SQLAlchemyError as e:
        raise InternalServerError(e.orig.args[1])
