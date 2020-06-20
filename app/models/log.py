from app import db, ma
import datetime


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(
        db.String(100), db.ForeignKey('product.id'), nullable=False
    )
    cellphone = db.Column(db.Integer, nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow()
    )

    def __init__(self, product_id, cellphone):
        self.product_id = product_id
        self.cellphone = cellphone


class LogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_id', 'cellphone', 'created')


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
