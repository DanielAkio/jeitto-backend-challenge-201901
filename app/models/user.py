from werkzeug.security import generate_password_hash
from app import db, ma
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, server_default='0')
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    removed = db.Column(db.DateTime)

    companies = db.relationship('Company', backref='user', lazy=True)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.admin = admin


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'username',
            'admin',
            'created',
            'updated',
            'removed'
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)
