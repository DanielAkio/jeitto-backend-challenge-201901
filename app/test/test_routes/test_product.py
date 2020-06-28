from app.models.product import Product
from app.models.company import Company
from unittest.mock import patch
from app import app
import unittest

company = Company('id', 1)
product = Product('id', 'company_id', 10.00)
product_dump = {
    'id': 'id',
    'company_id': 'company_id',
    'value': 10.00,
    'created': 'created',
    'updated': 'updated',
    'removed': 'removed'
}


def user_dump(id=1):
    user_dump = {
        'id': id,
        'access': 'access',
        'username': 'username',
        'created': 'created',
        'updated': 'updated',
        'removed': 'removed'
    }
    return user_dump


class TestProductFind(unittest.TestCase):

    @patch(
        'app.views.product.find',
        return_value=[product_dump, product_dump, product_dump]
    )
    @patch('app.views.helper._token_required', return_value=user_dump())
    def test_success(self, mock_token, mock_find):
        with app.test_client() as c:
            response = c.get('/CompanyProducts')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)

    @patch('app.views.product.find', return_value=None)
    @patch('app.views.helper._token_required', return_value=user_dump())
    def test_none_find(self, mock_token, mock_find):
        with app.test_client() as c:
            response = c.get('/CompanyProducts')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)


class TestProductCreate(unittest.TestCase):

    @patch('app.views.product.create', return_value=product_dump)
    @patch('app.routes.product.request')
    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch('app.views.helper._request_json_must_have', return_value=None)
    def test_success(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_company_id,
        mock_request,
        mock_create
    ):
        mock_request.json = {'id': 'id', 'value': 10.00}
        with app.test_client() as c:
            response = c.post('/CompanyProducts/id')
            self.assertEqual(response.status_code, 201)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert mock_create.called

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch('app.views.helper._request_json_must_have', return_value=None)
    def test_none_find_by_company_id(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.post('/CompanyProducts/id')
            self.assertEqual(response.status_code, 404)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_company_id.called

    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    @patch('app.views.helper._request_json_must_have', return_value=None)
    def test_not_owner(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.post('/CompanyProducts/id')
            self.assertEqual(response.status_code, 401)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_company_id.called


class TestProductUpdate(unittest.TestCase):

    @patch('app.views.product.update', return_value=product_dump)
    @patch('app.routes.product.request')
    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch('app.views.helper._request_json_must_have_one', return_value=None)
    def test_success(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id,
        mock_request,
        mock_update
    ):
        mock_request.json = {'id': 'id', 'value': 10.00}
        with app.test_client() as c:
            response = c.put('/CompanyProducts/id')
            self.assertEqual(response.status_code, 200)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called
        assert mock_update.called

    @patch('app.views.product.find_by_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch('app.views.helper._request_json_must_have_one', return_value=None)
    def test_none_find_by_id(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_id
    ):
        with app.test_client() as c:
            response = c.put('/CompanyProducts/id')
            self.assertEqual(response.status_code, 404)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch('app.views.helper._request_json_must_have_one', return_value=None)
    def test_none_find_by_company_id(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.put('/CompanyProducts/id')
            self.assertEqual(response.status_code, 404)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called

    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    @patch('app.views.helper._request_json_must_have_one', return_value=None)
    def test_not_owner(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.put('/CompanyProducts/id')
            self.assertEqual(response.status_code, 401)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called


class TestProductLogicalDelete(unittest.TestCase):

    @patch('app.views.product.logical_delete', return_value=product_dump)
    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_success(
        self,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id,
        mock_logical_delete
    ):
        with app.test_client() as c:
            response = c.delete('/CompanyProducts/id')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called
        assert mock_logical_delete.called

    @patch('app.views.product.find_by_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_none_find_by_id(
        self,
        mock_token,
        mock_find_by_id
    ):
        with app.test_client() as c:
            response = c.delete('/CompanyProducts/id')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_id.called

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_none_find_by_company_id(
        self,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.delete('/CompanyProducts/id')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called

    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    def test_not_owner(
        self,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id,
    ):
        with app.test_client() as c:
            response = c.delete('/CompanyProducts/id')
            self.assertEqual(response.status_code, 401)
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called


class TestProductLogicalRestore(unittest.TestCase):

    @patch('app.views.product.logical_restore', return_value=product_dump)
    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_success(
        self,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id,
        mock_logical_restore
    ):
        with app.test_client() as c:
            response = c.put('/CompanyProductsRestore/id')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called
        assert mock_logical_restore.called

    @patch('app.views.product.find_by_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_none_find_by_id(
        self,
        mock_token,
        mock_find_by_id
    ):
        with app.test_client() as c:
            response = c.put('/CompanyProductsRestore/id')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_id.called

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_none_find_by_company_id(
        self,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.put('/CompanyProductsRestore/id')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called

    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch('app.views.product.find_by_id', return_value=product)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    def test_not_owner(
        self,
        mock_token,
        mock_find_by_id,
        mock_find_by_company_id,
    ):
        with app.test_client() as c:
            response = c.put('/CompanyProductsRestore/id')
            self.assertEqual(response.status_code, 401)
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_find_by_company_id.called
