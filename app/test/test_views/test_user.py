from werkzeug.exceptions import InternalServerError, Conflict
from schema import Schema, Or, Use
from app.models.user import User
from unittest.mock import patch
from random import randrange
from app.views.user import (
    find_by_username,
    logical_restore,
    logical_delete,
    find_by_id,
    create,
    update,
    access,
    find
)
from sqlalchemy.exc import (
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    IntegrityError,
    InternalError,
    DataError
)
import unittest

user = User('username', 'password', 'access')
integrity_error = IntegrityError('Mock', 'mock', Exception('mock', 'mock'))
aleatory_errors = [
    DataError('Mock', 'mock', Exception('mock', 'mock')),
    OperationalError('Mock', 'mock', Exception('mock', 'mock')),
    InternalError('Mock', 'mock', Exception('mock', 'mock')),
    ProgrammingError('Mock', 'mock', Exception('mock', 'mock')),
    NotSupportedError('Mock', 'mock', Exception('mock', 'mock'))
]

user_validate = Schema({
    'id': Or(int, None),
    'updated': Or(str, None),
    'created': Or(str, None),
    'access': Or(str, None),
    'username': Use(str),
    'removed': Or(str, None)
})

user_list_validate = Schema([{
    'id': Or(int, None),
    'updated': Or(str, None),
    'created': Or(str, None),
    'access': Or(str, None),
    'username': Use(str),
    'removed': Or(str, None)
}])


class TestFind(unittest.TestCase):

    @patch('app.views.user.m_User')
    def test_success(self, mock_User):
        mock_User.query.all.return_value = [user, user, user]
        response = find()
        assert mock_User.query.all.called
        assert user_list_validate.validate(response)

    @patch('app.views.user.m_User')
    def test_success_none(self, mock_User):
        mock_User.query.all.return_value = None
        response = find()
        assert mock_User.query.all.called
        assert response == {}


class TestFindById(unittest.TestCase):

    @patch('app.views.user.m_User')
    def test_success(self, mock_User):
        mock_User.query.get.return_value = user
        response = find_by_id(1, json_response=False)
        assert isinstance(response, User)

    @patch('app.views.user.m_User')
    def test_success_json(self, mock_User):
        mock_User.query.get.return_value = user
        response = find_by_id(1)
        assert mock_User.query.get.called
        assert user_validate.validate(response)


class TestFindByUsername(unittest.TestCase):

    @patch('app.views.user.m_User')
    def test_success(self, mock_User):
        mock_User.query.filter_by().first.return_value = user
        response = find_by_username('username', json_response=False)
        assert isinstance(response, User)

    @patch('app.views.user.m_User')
    def test_success_json(self, mock_User):
        mock_User.query.filter_by().first.return_value = user
        response = find_by_username('username')
        assert mock_User.query.filter_by().first
        assert user_validate.validate(response)


class TestCreate(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    @patch('app.db.session.add', return_value=None)
    def test_success(self, mock_add, mock_commit):
        response = create(user)
        assert mock_add.called
        assert mock_commit.called
        assert user_validate.validate(response)

    @patch('app.db.session.add', side_effect=integrity_error)
    def test_failed_sql_alchemy_exception_integrity(self, mock_add):
        with self.assertRaises(Conflict):
            create(user)

    @patch('app.db.session.add', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            create(user)


class TestUpdate(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    @patch('app.views.user.request')
    def test_success(self, mock_request, mock_commit):
        mock_request.json = {'password': 'password', 'username': 'username'}
        response = update(user)
        assert mock_commit.called
        assert user_validate.validate(response)

    @patch('app.db.session.commit', side_effect=integrity_error)
    @patch('app.views.user.request')
    def test_failed_sql_alchemy_exception_integrity(
        self, mock_request, mock_add
    ):
        mock_request.json = {}
        with self.assertRaises(Conflict):
            update(user)

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    @patch('app.views.user.request')
    def test_failed_sql_alchemy_exception(self, mock_request, mock_add):
        mock_request.json = {}
        with self.assertRaises(InternalServerError):
            update(user)


class TestLogicalDelete(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    def test_success(self, mock_commit):
        response = logical_delete(user)
        assert mock_commit.called
        assert user_validate.validate(response)
        assert response['removed'] is not None

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            logical_delete(user)


class TestLogicalRestore(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    def test_success(self, mock_commit):
        response = logical_restore(user)
        assert mock_commit.called
        assert user_validate.validate(response)
        assert response['removed'] is None

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            logical_restore(user)


class TestAccess(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    @patch('app.views.user.request')
    def test_success(self, mock_request, mock_commit):
        mock_request.json = {'access': 'access'}
        response = access(user)
        assert mock_commit.called
        assert user_validate.validate(response)
        assert response['access'] == 'access'

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    @patch('app.views.user.request')
    def test_failed_sql_alchemy_exception(self, mock_request, mock_add):
        mock_request.json = {'access': 'access'}
        with self.assertRaises(InternalServerError):
            access(user)
