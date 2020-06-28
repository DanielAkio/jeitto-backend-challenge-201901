from unittest.mock import patch
from app import app
import unittest

log_dump = {
    'id': 'id',
    'product_id': 'product_id',
    'company_id': 'company_id',
    'user_id': 1,
    'phone_number': 'phone_number',
    'value': 99.99,
    'created': 'created'
}

user_dump = {
    'id': 1,
    'access': 'access',
    'username': 'username',
    'created': 'created',
    'updated': 'updated',
    'removed': 'removed'
}

product_dump = {
    'id': 'id',
    'company_id': 'company_id',
    'value': 99.99,
    'created': 'created',
    'updated': 'updated',
    'removed': 'removed'
}


class TestRechargeFind(unittest.TestCase):

    @patch('app.views.log.find', return_value=[log_dump, log_dump, log_dump])
    @patch('app.routes.recharge.request')
    @patch('app.views.helper._token_required', return_value=None)
    def test_success(self, mock_token, mock_request, mock_find):
        mock_request.args.get.return_value = 'id'
        with app.test_client() as c:
            response = c.get('/PhoneRecharges')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)

    @patch('app.routes.recharge.request')
    @patch('app.views.helper._token_required', return_value=None)
    def test_whitout_id_and_phone_number(
        self,
        mock_token,
        mock_request
    ):
        mock_request.args.get.return_value = None
        with app.test_client() as c:
            response = c.get('/PhoneRecharges')
            self.assertEqual(response.status_code, 422)
        assert mock_token.called
        assert isinstance(response.data, bytes)

    @patch('app.views.log.find', return_value=None)
    @patch('app.routes.recharge.request')
    @patch('app.views.helper._token_required', return_value=None)
    def test_none_find(self, mock_token, mock_request, mock_find):
        mock_request.args.get.return_value = 'id'
        with app.test_client() as c:
            response = c.get('/PhoneRecharges')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)


class TestRecharge(unittest.TestCase):

    @patch('app.views.log.create', return_value=log_dump)
    @patch('app.views.product.find_by_id', return_value=product_dump)
    @patch('app.routes.recharge.request')
    @patch('app.views.helper._request_json_must_have', return_value=None)
    @patch('app.views.helper._token_required', return_value=user_dump)
    def test_success(
        self,
        mock_token,
        mock_must_have,
        mock_request,
        mock_find_by_id,
        mock_create
    ):
        mock_request.json = {
            'product_id': 'product_id',
            'phone_number': 'phone_number'
        }
        with app.test_client() as c:
            response = c.post('/PhoneRecharges')
            self.assertEqual(response.status_code, 201)
        assert mock_token.called
        assert mock_must_have.called
        assert mock_find_by_id.called
        assert mock_create.called

    @patch('app.views.product.find_by_id', return_value=None)
    @patch('app.routes.recharge.request')
    @patch('app.views.helper._request_json_must_have', return_value=None)
    @patch('app.views.helper._token_required', return_value=user_dump)
    def test_none_find_by_id(
        self,
        mock_token,
        mock_must_have,
        mock_request,
        mock_find_by_id
    ):
        mock_request.json = {'product_id': 'product_id'}
        with app.test_client() as c:
            response = c.post('/PhoneRecharges')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_must_have.called
        assert mock_find_by_id.called
