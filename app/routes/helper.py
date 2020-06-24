from ..views import helper
from flask import jsonify
from app import app


@app.route('/Auth', methods=['POST'])
def helper_auth():
    return jsonify(helper.auth())
