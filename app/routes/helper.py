from ..views import helper
from app import app


@app.route('/Auth', methods=['POST'])
def helper_auth():
    return helper.auth()
