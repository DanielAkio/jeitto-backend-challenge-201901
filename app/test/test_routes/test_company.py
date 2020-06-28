from app.models.company import Company
from unittest.mock import patch
from app import app
import unittest

company = Company('id', 1)
company_dump = {
    'id': 'id',
    'user_id': 1,
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


class TestCompanyFind(unittest.TestCase):

    @patch(
        'app.views.company.find',
        return_value=[company_dump, company_dump, company_dump]
    )
    @patch('app.views.helper._token_admin_required', return_value=None)
    def test_success(self, mock_token, mock_find):
        with app.test_client() as c:
            response = c.get('/Company')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find', return_value=None)
    @patch('app.views.helper._token_admin_required', return_value=None)
    def test_none_find(self, mock_token, mock_find):
        with app.test_client() as c:
            response = c.get('/Company')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)


class TestCompanyFindById(unittest.TestCase):

    @patch('app.views.company.find_by_company_id', return_value=company_dump)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_success(self, mock_token, mock_find_by_company_id):
        with app.test_client() as c:
            response = c.get('/Company/id')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_token.mock_find_by_company_id
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_none_find_by_company_id(
        self,
        mock_token,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.get('/Company/id')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_token.mock_find_by_company_id
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=company_dump)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    def test_not_owner(
        self,
        mock_token,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.get('/Company/id')
            self.assertEqual(response.status_code, 401)
        assert mock_token.called
        assert mock_token.mock_find_by_company_id
        assert isinstance(response.data, bytes)


class TestCompanyCreate(unittest.TestCase):

    @patch('app.views.company.create', return_value=company_dump)
    @patch('app.routes.company.request')
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch(
        'app.views.helper._request_json_must_have',
        return_value=None
    )
    def test_success(
        self,
        mock_must_have,
        mock_token,
        mock_request,
        mock_create
    ):
        mock_request.json = {'id': 'id'}
        with app.test_client() as c:
            response = c.post('/Company')
            self.assertEqual(response.status_code, 201)
        assert mock_token.called
        assert mock_must_have.called
        assert mock_create.called
        assert isinstance(response.data, bytes)


class TestCompanyUpdate(unittest.TestCase):

    @patch('app.views.company.update', return_value=company_dump)
    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch(
        'app.views.helper._request_json_must_have_one',
        return_value=None
    )
    def test_success(
        self,
        mock_must_have_one,
        mock_token,
        mock_find_by_company_id,
        mock_update
    ):
        with app.test_client() as c:
            response = c.put('/Company/id')
            self.assertEqual(response.status_code, 200)
        assert mock_must_have_one.called
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert mock_update.called
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    @patch(
        'app.views.helper._request_json_must_have_one',
        return_value=None
    )
    def test_none_find_by_company_id(
        self,
        mock_must_have_one,
        mock_token,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.put('/Company/id')
            self.assertEqual(response.status_code, 404)
        assert mock_must_have_one.called
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    @patch(
        'app.views.helper._request_json_must_have_one',
        return_value=None
    )
    def test_not_owner(
        self,
        mock_must_have_one,
        mock_token,
        mock_find_by_company_id
    ):
        with app.test_client() as c:
            response = c.put('/Company/id')
            self.assertEqual(response.status_code, 401)
        assert mock_must_have_one.called
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert isinstance(response.data, bytes)


class TestCompanyLogicalDelete(unittest.TestCase):

    @patch('app.views.company.logical_delete', return_value=company_dump)
    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_success(
        self,
        mock_token,
        mock_find_by_company_id,
        mock_logical_delete
    ):
        with app.test_client() as c:
            response = c.delete('/Company/id')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert mock_logical_delete.called
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_none_find_by_company_id(
        self,
        mock_token,
        mock_find_by_company_id,
    ):
        with app.test_client() as c:
            response = c.delete('/Company/id')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    def test_not_owner(
        self,
        mock_token,
        mock_find_by_company_id,
    ):
        with app.test_client() as c:
            response = c.delete('/Company/id')
            self.assertEqual(response.status_code, 401)
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert isinstance(response.data, bytes)


class TestCompanyLogicalRestore(unittest.TestCase):

    @patch('app.views.company.logical_restore', return_value=company_dump)
    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_success(
        self,
        mock_token,
        mock_find_by_company_id,
        mock_logical_restore
    ):
        with app.test_client() as c:
            response = c.put('/CompanyRestore/id')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert mock_logical_restore.called
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=None)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump()
    )
    def test_none_find_by_company_id(
        self,
        mock_token,
        mock_find_by_company_id,
    ):
        with app.test_client() as c:
            response = c.put('/CompanyRestore/id')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert isinstance(response.data, bytes)

    @patch('app.views.company.find_by_company_id', return_value=company)
    @patch(
        'app.views.helper._token_owner_or_admin_required',
        return_value=user_dump(2)
    )
    def test_not_owner(
        self,
        mock_token,
        mock_find_by_company_id,
    ):
        with app.test_client() as c:
            response = c.put('/CompanyRestore/id')
            self.assertEqual(response.status_code, 401)
        assert mock_token.called
        assert mock_find_by_company_id.called
        assert isinstance(response.data, bytes)
