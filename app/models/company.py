from app import db, ma


class Company(db.Model):
    company_id = db.Column(db.String(100), primary_key=True, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False
    )

    products = db.relationship('Product', backref='company', lazy=True)

    def __init__(self, company_id, user_id):
        self.company_id = company_id
        self.user_id = user_id


class CompanySchema(ma.Schema):
    class Meta:
        fields = ('company_id', 'user_id')


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
