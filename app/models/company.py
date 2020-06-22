from app import db, ma
import datetime


class Company(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow()
    )
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    removed = db.Column(db.DateTime)

    products = db.relationship('Product', backref='company', lazy=True)
    logs = db.relationship('Log', backref='company', lazy=True)

    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id


class CompanySchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'created', 'updated', 'removed')


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
