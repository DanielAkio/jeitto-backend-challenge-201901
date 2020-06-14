from ..views import helper
from app import app


@app.route('/Auth', methods=['POST'])
def auth():
    return helper.auth()
