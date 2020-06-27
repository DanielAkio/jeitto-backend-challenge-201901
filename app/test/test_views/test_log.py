from schema import Schema, Use, Or
from unittest.mock import patch
from app.views.log import find
from app.models.log import Log
import unittest
import uuid


log = Log(
    user_id=1,
    product_id='product_id',
    company_id='company_id',
    phone_number=5511999999999,
    value=10.00
)

log_validate = Schema({
    'id': Use(str),
    'user_id': Use(int),
    'product_id': Use(str),
    'company_id': Use(str),
    'phone_number': Use(int),
    'value': Use(float),
    'created': Or(str, None)
})

logs_validate = Schema([{
    'id': Use(str),
    'user_id': Use(int),
    'product_id': Use(str),
    'company_id': Use(str),
    'phone_number': Use(int),
    'value': Use(float),
    'created': Or(str, None)
}])


class TestFind(unittest.TestCase):

    @patch('app.views.log.m_Log')
    @patch('app.views.log.request')
    def test_with_id_success(self, mock_request, mock_Log):
        mock_request.args.get.return_value = {'id': str(uuid.uuid1())}
        mock_Log.query.get.return_value = log
        response = find()
        assert mock_request.args.get.called
        assert mock_Log.query.get.called
        assert log_validate.validate(response)

    @patch('app.views.log.m_Log')
    @patch('app.views.log.request')
    def test_without_id_success(self, mock_request, mock_Log):
        mock_request.args.get.return_value = None
        mock_Log.query.filter_by().all.return_value = [log, log, log]
        response = find()
        assert mock_request.args.get.called
        assert mock_Log.query.filter_by().all.called
        assert logs_validate.validate(response)

    @patch('app.views.log.m_Log')
    @patch('app.views.log.request')
    def test_with_id_none_log(self, mock_request, mock_Log):
        mock_request.args.get.return_value = {'id': str(uuid.uuid1())}
        mock_Log.query.get.return_value = None
        response = find()
        assert mock_request.args.get.called
        assert mock_Log.query.get.called
        assert not response

    @patch('app.views.log.m_Log')
    @patch('app.views.log.request')
    def test_without_id_none_logs(self, mock_request, mock_Log):
        mock_request.args.get.return_value = None
        mock_Log.query.filter_by().all.return_value = None
        response = find()
        assert mock_request.args.get.called
        assert mock_Log.query.filter_by().all.called
        assert not response
