from app import db, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, server_default='0')

    companies = db.relationship('Company', backref='user', lazy=True)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = password
        self.admin = admin


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'admin')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
