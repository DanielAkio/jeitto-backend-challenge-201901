from werkzeug.exceptions import InternalServerError, Conflict
from app.models.company import Company
from schema import Schema, Or, Use
from unittest.mock import patch
from app.views.company import (
    find_by_company_id,
    logical_restore,
    logical_delete,
    create,
    update,
    find
)
from random import randrange
from sqlalchemy.exc import (
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    IntegrityError,
    InternalError,
    DataError
)
import unittest

company = Company('id', user_id=1)
integrity_error = IntegrityError('Mock', 'mock', Exception('mock', 'mock'))
aleatory_errors = [
    DataError('Mock', 'mock', Exception('mock', 'mock')),
    OperationalError('Mock', 'mock', Exception('mock', 'mock')),
    InternalError('Mock', 'mock', Exception('mock', 'mock')),
    ProgrammingError('Mock', 'mock', Exception('mock', 'mock')),
    NotSupportedError('Mock', 'mock', Exception('mock', 'mock'))
]

company_validate = Schema({
    'id': Use(str),
    'user_id': Use(int),
    'created': Or(str, None),
    'updated': Or(str, None),
    'removed': Or(str, None)
})

company_list_validate = Schema([{
    'id': Use(str),
    'user_id': Use(int),
    'created': Or(str, None),
    'updated': Or(str, None),
    'removed': Or(str, None)
}])


class TestFind(unittest.TestCase):

    @patch('app.views.company.m_Company')
    def test_success(self, mock_Company):
        mock_Company.query.all.return_value = [company, company, company]
        response = find()
        assert mock_Company.query.all.called
        assert company_list_validate.validate(response)

    @patch('app.views.company.m_Company')
    def test_success_none(self, mock_Company):
        mock_Company.query.all.return_value = None
        response = find()
        assert mock_Company.query.all.called
        assert response == {}


class TestFindByCompanyId(unittest.TestCase):

    @patch('app.views.company.m_Company')
    def test_success(self, mock_Company):
        mock_Company.query.get.return_value = company
        response = find_by_company_id(1, json_response=False)
        assert isinstance(response, Company)

    @patch('app.views.company.m_Company')
    def test_success_json(self, mock_Company):
        mock_Company.query.get.return_value = company
        response = find_by_company_id(1)
        assert mock_Company.query.get.called
        assert company_validate.validate(response)


class TestCreate(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    @patch('app.db.session.add', return_value=None)
    def test_success(self, mock_add, mock_commit):
        response = create(company)
        assert mock_add.called
        assert mock_commit.called
        assert company_validate.validate(response)

    @patch('app.db.session.add', side_effect=integrity_error)
    def test_failed_sql_alchemy_exception_integrity(self, mock_add):
        with self.assertRaises(Conflict):
            create(company)

    @patch('app.db.session.add', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            create(company)


class TestUpdate(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    @patch('app.views.company.request')
    def test_success(self, mock_request, mock_commit):
        mock_request.json = {'id': 'id', 'user_id': 1}
        response = update(company)
        assert mock_commit.called
        assert company_validate.validate(response)

    @patch('app.db.session.commit', side_effect=integrity_error)
    @patch('app.views.company.request')
    def test_failed_sql_alchemy_exception_integrity(
        self, mock_request, mock_add
    ):
        mock_request.json = {}
        with self.assertRaises(Conflict):
            update(company)

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    @patch('app.views.company.request')
    def test_failed_sql_alchemy_exception(self, mock_request, mock_add):
        mock_request.json = {}
        with self.assertRaises(InternalServerError):
            update(company)


class TestLogicalDelete(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    def test_success(self, mock_commit):
        response = logical_delete(company)
        assert mock_commit.called
        assert company_validate.validate(response)
        assert response['removed'] is not None

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            logical_delete(company)


class TestLogicalRestore(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    def test_success(self, mock_commit):
        response = logical_restore(company)
        assert mock_commit.called
        assert company_validate.validate(response)
        assert response['removed'] is None

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            logical_restore(company)
