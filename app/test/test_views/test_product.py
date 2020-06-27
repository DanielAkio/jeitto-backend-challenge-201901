from werkzeug.exceptions import InternalServerError, Conflict
from app.models.product import Product
from schema import Schema, Or, Use
from .test_company import company
from unittest.mock import patch
from app.views.product import (
    logical_delete,
    logical_restore,
    find_by_id,
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
from .test_user import user
import unittest

product = Product('id', company_id='company_id', value=10.00)
integrity_error = IntegrityError('Mock', 'mock', Exception('mock', 'mock'))
aleatory_errors = [
    DataError('Mock', 'mock', Exception('mock', 'mock')),
    OperationalError('Mock', 'mock', Exception('mock', 'mock')),
    InternalError('Mock', 'mock', Exception('mock', 'mock')),
    ProgrammingError('Mock', 'mock', Exception('mock', 'mock')),
    NotSupportedError('Mock', 'mock', Exception('mock', 'mock'))
]

product_validate = Schema({
    'id': Use(str),
    'company_id': Use(str),
    'value': Use(float),
    'created': Or(str, None),
    'updated': Or(str, None),
    'removed': Or(str, None)
})

companies_products_validate = Schema([{
    'id': Use(str),
    'user_id': Use(int),
    'created': Or(str, None),
    'updated': Or(str, None),
    'removed': Or(str, None),
    'products': Or([{
        'id': Use(str),
        'company_id': Use(str),
        'value': Use(float),
        'created': Or(str, None),
        'updated': Or(str, None),
        'removed': Or(str, None)
    }], {})
}])

company_products_validate = Schema({
    'id': Use(str),
    'user_id': Use(int),
    'created': Or(str, None),
    'updated': Or(str, None),
    'removed': Or(str, None),
    'products': Or([{
        'id': Use(str),
        'company_id': Use(str),
        'value': Use(float),
        'created': Or(str, None),
        'updated': Or(str, None),
        'removed': Or(str, None)
    }], {})
})


class TestFind(unittest.TestCase):

    @patch('app.views.product.m_Product')
    @patch('app.views.product.m_Company')
    @patch('app.views.product.request')
    def test_with_id_success(
        self,
        mock_request,
        mock_Company,
        mock_Product
    ):
        mock_request.args.get.return_value = {'company_id': 'company_id'}
        mock_Company.query.filter_by().first.return_value = company
        mock_Product.query.filter_by().all.return_value = [product, product]
        response = find(user)
        assert mock_request.args.get.called
        assert mock_Company.query.filter_by().first.called
        assert mock_Product.query.filter_by().all.called
        assert company_products_validate.validate(response)

    @patch('app.views.product.m_Product')
    @patch('app.views.product.m_Company')
    @patch('app.views.product.request')
    def test_without_id_success(
        self,
        mock_request,
        mock_Company,
        mock_Product
    ):
        mock_request.args.get.return_value = None
        mock_Company.query.all.return_value = [company, company, company]
        mock_Product.query.filter_by().all.return_value = [product, product]
        response = find(user)
        assert mock_request.args.get.called
        assert mock_Company.query.all.called
        assert mock_Product.query.filter_by().all.called
        assert companies_products_validate.validate(response)

    @patch('app.views.product.m_Company')
    @patch('app.views.product.request')
    def test_with_id_none_company(
        self,
        mock_request,
        mock_Company
    ):
        mock_request.args.get.return_value = {'company_id': 'company_id'}
        mock_Company.query.filter_by().first.return_value = None
        response = find(user)
        assert mock_request.args.get.called
        assert mock_Company.query.filter_by().first.called
        assert response is None

    @patch('app.views.product.m_Company')
    @patch('app.views.product.request')
    def test_without_id_none_companies(
        self,
        mock_request,
        mock_Company
    ):
        mock_request.args.get.return_value = None
        mock_Company.query.all.return_value = None
        response = find(user)
        assert mock_request.args.get.called
        assert mock_Company.query.all.called
        assert response is None

    @patch('app.views.product.m_Product')
    @patch('app.views.product.m_Company')
    @patch('app.views.product.request')
    def test_with_id_none_products(
        self,
        mock_request,
        mock_Company,
        mock_Product
    ):
        mock_request.args.get.return_value = {'company_id': 'company_id'}
        mock_Company.query.filter_by().first.return_value = company
        mock_Product.query.filter_by().all.return_value = None
        response = find(user)
        assert mock_request.args.get.called
        assert mock_Company.query.filter_by().first.called
        assert mock_Product.query.filter_by().all.called
        assert company_products_validate.validate(response)
        assert not response['products']

    @patch('app.views.product.m_Product')
    @patch('app.views.product.m_Company')
    @patch('app.views.product.request')
    def test_without_id_none_products(
        self,
        mock_request,
        mock_Company,
        mock_Product
    ):
        mock_request.args.get.return_value = None
        mock_Company.query.all.return_value = [company, company, company]
        mock_Product.query.filter_by().all.return_value = None
        response = find(user)
        assert mock_request.args.get.called
        assert mock_Company.query.all.called
        assert mock_Product.query.filter_by().all.called
        assert companies_products_validate.validate(response)
        for _company in response:
            assert not _company['products']


class TestFindById(unittest.TestCase):

    @patch('app.views.product.m_Product')
    def test_success(self, mock_Product):
        mock_Product.query.get.return_value = product
        response = find_by_id('id', json_response=False)
        assert mock_Product.query.get.called
        assert isinstance(response, Product)

    @patch('app.views.product.m_Product')
    def test_success_json(self, mock_Product):
        mock_Product.query.get.return_value = product
        response = find_by_id('id')
        assert mock_Product.query.get.called
        assert product_validate.validate(response)


class TestCreate(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    @patch('app.db.session.add', return_value=None)
    def test_success(self, mock_add, mock_commit):
        response = create(product)
        assert mock_add.called
        assert mock_commit.called
        assert product_validate.validate(response)

    @patch('app.db.session.add', side_effect=integrity_error)
    def test_failed_sql_alchemy_exception_integrity(self, mock_add):
        with self.assertRaises(Conflict):
            create(product)

    @patch('app.db.session.add', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            create(product)


class TestUpdate(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    @patch('app.views.product.request')
    def test_success(self, mock_request, mock_commit):
        mock_request.json = {'id': 'id', 'value': 10.00}
        response = update(product)
        assert mock_commit.called
        assert product_validate.validate(response)

    @patch('app.db.session.commit', side_effect=integrity_error)
    @patch('app.views.product.request')
    def test_failed_sql_alchemy_exception_integrity(
        self, mock_request, mock_add
    ):
        mock_request.json = {}
        with self.assertRaises(Conflict):
            update(product)

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    @patch('app.views.product.request')
    def test_failed_sql_alchemy_exception(self, mock_request, mock_add):
        mock_request.json = {}
        with self.assertRaises(InternalServerError):
            update(product)


class TestLogicalDelete(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    def test_success(self, mock_commit):
        response = logical_delete(product)
        assert mock_commit.called
        assert product_validate.validate(response)
        assert response['removed'] is not None

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            logical_delete(product)


class TestLogicalRestore(unittest.TestCase):

    @patch('app.db.session.commit', return_value=None)
    def test_success(self, mock_commit):
        response = logical_restore(product)
        assert mock_commit.called
        assert product_validate.validate(response)
        assert response['removed'] is None

    @patch('app.db.session.commit', side_effect=aleatory_errors[randrange(5)])
    def test_failed_sql_alchemy_exception(self, mock_add):
        with self.assertRaises(InternalServerError):
            logical_restore(product)
