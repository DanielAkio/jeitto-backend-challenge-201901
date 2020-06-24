from app.views.database import is_empty, drop_all, create_all
from werkzeug.exceptions import InternalServerError
from unittest.mock import patch
import unittest


class TestIsEmpty(unittest.TestCase):

    class WithTables:
        def get_table_names(self):
            return ['table_0', 'table_1']

    class Empty:
        def get_table_names(self):
            return []

    @patch('app.db.inspect', return_value=WithTables())
    def test_with_tables(self, mock_inspect):
        assert is_empty() is False

    @patch('app.db.inspect', return_value=Empty())
    def test_empty(self, mock_inspect):
        assert is_empty() is True


class TestCreateAll(unittest.TestCase):

    @patch('app.db.create_all', return_value=None)
    def test_success(self, mock_create_all):
        assert not create_all()

    @patch('app.db.create_all', side_effect=Exception())
    def test_exception(self, mock_create_all):
        with self.assertRaises(InternalServerError):
            create_all()


class TestDropAll(unittest.TestCase):

    @patch('app.db.drop_all', return_value=None)
    def test_success(self, mock_drop_all):
        assert not drop_all()

    @patch('app.db.drop_all', side_effect=Exception())
    def test_exception(self, mock_drop_all):
        with self.assertRaises(InternalServerError):
            drop_all()
