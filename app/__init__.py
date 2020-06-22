from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)


from .models import user, company, product, log
from .routes import (
    database, helper, user, company, product, recharge
)
