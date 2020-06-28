from app.models.user import User
from unittest.mock import patch
from app import app
import unittest

user = User('admin', 'admin', 'admin')


class TestDatabaseCreateAll(unittest.TestCase):

    @patch('app.routes.database.v_user.create', return_value=None)
    @patch('app.routes.database.m_user.User', return_value=user)
    @patch('app.routes.database.v_database')
    def test_success(self, mock_database, mock_User, mock_create):
        mock_database.is_empty.return_value = True
        mock_database.create_all.return_value = None
        with app.test_client() as c:
            response = c.post('/DatabaseCreate')
            self.assertEqual(response.status_code, 201)
        assert mock_database.is_empty.called
        assert mock_database.create_all.called
        assert mock_User.called
        assert mock_create.called
        assert isinstance(response.data, bytes)

    @patch('app.routes.database.v_database.is_empty', return_value=False)
    def test_false_is_empty(self, mock_is_empty):
        with app.test_client() as c:
            response = c.post('/DatabaseCreate')
            self.assertEqual(response.status_code, 400)


class TestDatabaseDropAll(unittest.TestCase):

    @patch(
        'app.routes.database.v_helper._token_admin_required',
        return_value=None
    )
    @patch('app.routes.database.v_database')
    def test_success(self, mock_database, mock_token):
        mock_database.is_empty.return_value = False
        mock_database.drop_all.return_value = None
        with app.test_client() as c:
            response = c.delete('/DatabaseDrop')
            self.assertEqual(response.status_code, 200)
        assert mock_token.called
        assert mock_database.is_empty.called
        assert mock_database.drop_all.called

    @patch(
        'app.routes.database.v_helper._token_admin_required',
        return_value=None
    )
    @patch('app.routes.database.v_database.is_empty', return_value=True)
    def test_false_is_empty(self, mock_is_empty, mock_token):
        with app.test_client() as c:
            response = c.delete('/DatabaseDrop')
            self.assertEqual(response.status_code, 400)
