from app import db, ma


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, server_default='0')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'admin')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
