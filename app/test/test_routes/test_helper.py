from unittest.mock import patch
from app import app
import unittest


class TestAuth(unittest.TestCase):

    @patch(
        'app.views.helper.auth',
        return_value={
            'expirate_date': 'expirate_date',
            'token': 'token'
        }
    )
    def test_success(self, mock_auth):
        with app.test_client() as c:
            response = c.post('/Auth')
            self.assertEqual(response.status_code, 200)
        assert isinstance(response.data, bytes)
