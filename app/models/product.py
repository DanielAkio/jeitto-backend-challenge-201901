from app import db, ma
import datetime


class Product(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False)
    company_id = db.Column(
        db.String(100), db.ForeignKey('company.company_id'), nullable=False
    )
    value = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())

    def __init__(self, company_id, owner_id):
        self.company_id = company_id
        self.owner_id = owner_id


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'company_id', 'value')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
