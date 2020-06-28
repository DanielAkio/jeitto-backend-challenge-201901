from app.models.user import User
from unittest.mock import patch
from app import app
import unittest

user = User('username', 'password', 'access')
user_dump = {
    'id': 1,
    'access': 'access',
    'username': 'username',
    'created': 'created',
    'updated': 'updated',
    'removed': 'removed'
}


class TestUserFind(unittest.TestCase):

    @patch(
        'app.views.user.find',
        return_value=[user_dump, user_dump, user_dump]
    )
    @patch(
        'app.views.helper._token_admin_required',
        return_value=None
    )
    def test_success(self, mock_token, mock_find):
        with app.test_client() as c:
            response = c.get('/User')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)

    @patch('app.views.user.find', return_value=None)
    @patch(
        'app.views.helper._token_admin_required',
        return_value=None
    )
    def test_none_find(self, mock_token, mock_find):
        with app.test_client() as c:
            response = c.get('/User')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find.called
        assert isinstance(response.data, bytes)


class TestUserFindById(unittest.TestCase):

    @patch('app.views.user.find_by_id', return_value=user_dump)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    def test_success(self, mock_token, mock_find_by_id):
        with app.test_client() as c:
            response = c.get('/User/1')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find_by_id.called
        assert isinstance(response.data, bytes)

    @patch('app.views.user.find_by_id', return_value=None)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    def test_none_find_by_id(self, mock_token, mock_find_by_id):
        with app.test_client() as c:
            response = c.get('/User/1')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_id.called
        assert isinstance(response.data, bytes)


class TestUserCreate(unittest.TestCase):

    @patch('app.views.user.create', return_value=user_dump)
    @patch('app.routes.user.request')
    @patch(
        'app.views.helper._request_json_must_have',
        return_value=None
    )
    def test_success(self, mock_token, mock_request, mock_create):
        mock_request.json = {'username': 'username', 'password': 'password'}
        with app.test_client() as c:
            response = c.post('/User')
            self.assertEqual(response.status_code, 201)
        assert mock_token.called
        assert mock_create.called
        assert isinstance(response.data, bytes)


class TestUserUpdate(unittest.TestCase):

    @patch('app.views.user.update', return_value=user_dump)
    @patch('app.views.user.find_by_id', return_value=user)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    @patch(
        'app.views.helper._request_json_must_have_one',
        return_value=None
    )
    def test_success(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_id,
        mock_update
    ):
        with app.test_client() as c:
            response = c.put('/User/1')
            self.assertEqual(response.status_code, 200)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_update.called
        assert isinstance(response.data, bytes)

    @patch('app.views.user.find_by_id', return_value=None)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    @patch(
        'app.views.helper._request_json_must_have_one',
        return_value=None
    )
    def test_none_find_by_id(
        self,
        mock_must_have,
        mock_token,
        mock_find_by_id
    ):
        with app.test_client() as c:
            response = c.put('/User/1')
            self.assertEqual(response.status_code, 404)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called
        assert isinstance(response.data, bytes)


class TestUserLogicalDelete(unittest.TestCase):

    @patch('app.views.user.logical_delete', return_value=user_dump)
    @patch('app.views.user.find_by_id', return_value=user)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    def test_success(self, mock_token, mock_find_by_id, mock_delete):
        with app.test_client() as c:
            response = c.delete('/User/1')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_delete.called
        assert isinstance(response.data, bytes)

    @patch('app.views.user.find_by_id', return_value=None)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    def test_none_find_by_id(
        self,
        mock_token,
        mock_find_by_id
    ):
        with app.test_client() as c:
            response = c.delete('/User/1')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_id.called
        assert isinstance(response.data, bytes)


class TestUserLogicalRestore(unittest.TestCase):

    @patch('app.views.user.logical_restore', return_value=user_dump)
    @patch('app.views.user.find_by_id', return_value=user)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    def test_success(self, mock_token, mock_find_by_id, mock_restore):
        with app.test_client() as c:
            response = c.put('/UserRestore/1')
            self.assertEqual(response.status_code, 200)

    @patch('app.views.user.find_by_id', return_value=None)
    @patch(
        'app.views.helper._token_yourself_or_admin_required',
        return_value=None
    )
    def test_none_find_by_id(
        self,
        mock_token,
        mock_find_by_id
    ):
        with app.test_client() as c:
            response = c.put('/UserRestore/1')
            self.assertEqual(response.status_code, 404)
        assert mock_token.called
        assert mock_find_by_id.called
        assert isinstance(response.data, bytes)


class TestUserAccess(unittest.TestCase):

    @patch('app.views.user.access', return_value=user_dump)
    @patch('app.views.user.find_by_id', return_value=user)
    @patch('app.routes.user.request')
    @patch(
        'app.views.helper._token_admin_required',
        return_value=None
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
        mock_find_by_id,
        mock_access
    ):
        mock_request.json = {'access': 'admin'}
        with app.test_client() as c:
            response = c.put('/UserAccess/1')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called
        assert mock_access.called
        assert isinstance(response.data, bytes)

    @patch('app.routes.user.request')
    @patch(
        'app.views.helper._token_admin_required',
        return_value=None
    )
    @patch(
        'app.views.helper._request_json_must_have',
        return_value=None
    )
    def test_wrong_access(self, mock_must_have, mock_token, mock_request):
        mock_request.json = {'access': 'access'}
        with app.test_client() as c:
            response = c.put('/UserAccess/1')
            self.assertEqual(response.status_code, 422)
        assert mock_must_have.called
        assert mock_token.called
        assert isinstance(response.data, bytes)

    @patch('app.views.user.find_by_id', return_value=None)
    @patch('app.routes.user.request')
    @patch(
        'app.views.helper._token_admin_required',
        return_value=None
    )
    @patch(
        'app.views.helper._request_json_must_have',
        return_value=None
    )
    def test_wrong_access(
        self,
        mock_must_have,
        mock_token,
        mock_request,
        mock_find_by_id
    ):
        mock_request.json = {'access': 'admin'}
        with app.test_client() as c:
            response = c.put('/UserAccess/1')
            self.assertEqual(response.status_code, 404)
        assert mock_must_have.called
        assert mock_token.called
        assert mock_find_by_id.called
        assert isinstance(response.data, bytes)
