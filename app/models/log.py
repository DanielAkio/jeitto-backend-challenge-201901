from app import db, ma
import datetime
import uuid


class Log(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(
        db.String(100), db.ForeignKey('product.id'), nullable=False
    )
    company_id = db.Column(
        db.String(100), db.ForeignKey('company.id'), nullable=False
    )
    value = db.Column(db.Float, nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow()
    )

    def __init__(self, user_id, product_id, company_id, phone_number, value):
        self.id = str(uuid.uuid1())
        self.user_id = user_id
        self.company_id = company_id
        self.product_id = product_id
        self.phone_number = phone_number
        self.value = value


class LogSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'user_id',
            'product_id',
            'company_id',
            'phone_number',
            'created',
            'value'
        )


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
