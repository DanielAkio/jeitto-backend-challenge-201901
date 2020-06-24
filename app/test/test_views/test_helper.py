from werkzeug.exceptions import (
    UnprocessableEntity,
    Unauthorized,
    NotFound
)
from unittest.mock import patch
from schema import Schema, Use
from app.views.helper import (
    token_yourself_or_admin_required,
    token_owner_or_admin_required,
    request_json_must_have_one,
    request_json_must_have,
    token_admin_required,
    token_required,
    auth
)
import unittest


class User:
    def __init__(self, access):
        self.id = 1
        self.access = access
        self.username = 'username'
        self.password = 'password'


user_dict_validate = Schema({
    'id': Use(int),
    'access': Use(str),
    'username': Use(str)
})

user_dict = {
    'id': 1,
    'access': 'access',
    'username': 'username'
}


def inject_kwargs(f):
    def wrapper(*args, **kwargs):
        kwargs['id'] = 1
        f(*args, **kwargs)
    return wrapper


class TestAuth(unittest.TestCase):

    success_schema = Schema({
        'token': Use(str),
        'expirate_date': Use(str)
    })

    class Authorization:
        username = 'username'
        password = 'password'

    @patch('app.views.helper.check_password_hash', return_value=True)
    @patch('app.views.user.find_by_username', return_value=User('common'))
    @patch('app.views.helper.request')
    def test_success(
        self,
        mock_request,
        mock_find_by_username,
        mock_check_password_hash
    ):
        mock_request.authorization = self.Authorization()
        response = auth()
        assert self.success_schema.validate(response)

    @patch('app.views.helper.request')
    def test_without_authorization(self, mock_request):
        mock_request.authorization = None
        with self.assertRaises(Unauthorized):
            auth()

    @patch('app.views.helper.request')
    def test_without_authorization_username(self, mock_request):
        mock_request.authorization = self.Authorization()
        mock_request.authorization.username = None
        with self.assertRaises(Unauthorized):
            auth()

    @patch('app.views.helper.request')
    def test_without_authorization_password(self, mock_request):
        mock_request.authorization = self.Authorization()
        mock_request.authorization.password = None
        with self.assertRaises(Unauthorized):
            auth()

    @patch('app.views.user.find_by_username', return_value=None)
    @patch('app.views.helper.request')
    def test_none_find_by_username(
        self,
        mock_request,
        mock_find_by_username
    ):
        mock_request.authorization = self.Authorization()
        with self.assertRaises(NotFound):
            auth()

    @patch('app.views.helper.check_password_hash', return_value=False)
    @patch('app.views.user.find_by_username', return_value=User('common'))
    @patch('app.views.helper.request')
    def test_failed_check_password_hash(
        self,
        mock_request,
        mock_find_by_username,
        mock_check_password_hash
    ):
        mock_request.authorization = self.Authorization()
        with self.assertRaises(Unauthorized):
            auth()


class TestTokenRequired(unittest.TestCase):

    @token_required()
    def function_without_return(self):
        pass

    @token_required(get_user=True)
    def function_with_return(self, user):
        return user

    @token_required(get_user=True, json_response=True)
    def function_with_return_json(self, user):
        return user

    @patch('app.views.helper.jwt.decode', return_value={'id': 1})
    @patch('app.views.helper.request')
    def test_success(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = 'token'
        response = self.function_without_return()
        assert not response

    @patch('app.views.user.find_by_id', return_value=User('common'))
    @patch('app.views.helper.jwt.decode', return_value={'id': 1})
    @patch('app.views.helper.request')
    def test_success_with_return(
        self,
        mock_request,
        mock_decode,
        mock_find_by_id
    ):
        mock_request.headers.get.return_value = 'token'
        response = self.function_with_return()
        assert isinstance(response, User)

    @patch('app.views.user.find_by_id', return_value=user_dict)
    @patch('app.views.helper.jwt.decode', return_value={'id': 1})
    @patch('app.views.helper.request')
    def test_success_with_return_json(
        self,
        mock_request,
        mock_decode,
        mock_find_by_id
    ):
        mock_request.headers.get.return_value = 'token'
        response = self.function_with_return()
        assert user_dict_validate.validate(response)

    @patch('app.views.helper.request')
    def test_without_headers_get(self, mock_request):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()

    @patch('app.views.helper.jwt.decode', side_effect=Exception())
    @patch('app.views.helper.request')
    def test_failed_decode(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()


class TestTokenAdminRequired(unittest.TestCase):

    @token_admin_required()
    def function_without_return(self):
        pass

    @token_admin_required(get_user=True)
    def function_with_return(self, user):
        return user

    @patch('app.views.helper.jwt.decode', return_value={'access': 'admin'})
    @patch('app.views.helper.request')
    def test_success(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = 'token'
        response = self.function_without_return()
        assert not response

    @patch('app.views.user.find_by_id', return_value=User('admin'))
    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'admin', 'id': 1}
    )
    @patch('app.views.helper.request')
    def test_success_with_return(
        self,
        mock_request,
        mock_decode,
        mock_find_by_id
    ):
        mock_request.headers.get.return_value = 'token'
        response = self.function_with_return()
        assert isinstance(response, User)

    @patch('app.views.helper.request')
    def test_without_headers_get(self, mock_request):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()

    @patch('app.views.helper.jwt.decode', side_effect=Exception())
    @patch('app.views.helper.request')
    def test_failed_decode(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()

    @patch('app.views.helper.jwt.decode', return_value={'access': 'not_admin'})
    @patch('app.views.helper.request')
    def test_not_admin(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = 'token'
        with self.assertRaises(Unauthorized):
            self.function_without_return()


class TestTokenYourselfOrAdminRequired(unittest.TestCase):

    @token_yourself_or_admin_required()
    def function_without_return(self, **kwargs):
        pass

    @token_yourself_or_admin_required(get_user=True)
    def function_with_return(self, user, **kwargs):
        return user

    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'admin', 'id': 1}
    )
    @patch('app.views.helper.request')
    def test_success_admin(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = 'token'
        kwargs = {'id': 1}
        response = self.function_without_return(**kwargs)
        assert not response

    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'common', 'id': 2}
    )
    @patch('app.views.helper.request')
    def test_success_yourself(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = 'token'
        kwargs = {'id': 2}
        response = self.function_without_return(**kwargs)
        assert not response

    @patch('app.views.user.find_by_id', return_value=User('admin'))
    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'admin', 'id': 1}
    )
    @patch('app.views.helper.request')
    def test_success_with_return(
        self,
        mock_request,
        mock_decode,
        mock_find_by_id
    ):
        mock_request.headers.get.return_value = 'token'
        kwargs = {'id': 1}
        response = self.function_with_return(**kwargs)
        assert isinstance(response, User)

    @patch('app.views.helper.request')
    def test_without_headers_get(self, mock_request):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()

    @patch('app.views.helper.jwt.decode', side_effect=Exception())
    @patch('app.views.helper.request')
    def test_failed_decode(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()

    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'common', 'id': 2}
    )
    @patch('app.views.helper.request')
    def test_not_admin_and_yourself(self, mock_decode, mock_request):
        mock_request.headers.get.return_value = 'token'
        kwargs = {'id': 1}
        with self.assertRaises(Unauthorized):
            self.function_without_return(**kwargs)


class TestTokenOwnerOrAdminRequired(unittest.TestCase):

    @token_owner_or_admin_required()
    def function_without_return(self):
        pass

    @token_owner_or_admin_required(get_user=True, json_response=False)
    def function_with_return(self, user):
        return user

    @token_owner_or_admin_required(get_user=True)
    def function_with_return_json(self, user):
        return user

    @patch('app.views.helper.jwt.decode', return_value={'access': 'admin'})
    @patch('app.views.helper.request')
    def test_success_admin(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = 'token'
        response = self.function_without_return()
        assert not response

    @patch('app.views.helper.jwt.decode', return_value={'access': 'owner'})
    @patch('app.views.helper.request')
    def test_success_owner(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = 'token'
        response = self.function_without_return()
        assert not response

    @patch('app.views.user.find_by_id', return_value=User('admin'))
    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'admin', 'id': 1})
    @patch('app.views.helper.request')
    def test_success_with_return(
        self,
        mock_request,
        mock_decode,
        mock_find_by_id
    ):
        mock_request.headers.get.return_value = 'token'
        response = self.function_with_return()
        assert isinstance(response, User)

    @patch('app.views.user.find_by_id', return_value=user_dict)
    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'admin', 'id': 1})
    @patch('app.views.helper.request')
    def test_success_with_return_json(
        self,
        mock_request,
        mock_decode,
        mock_find_by_id
    ):
        mock_request.headers.get.return_value = 'token'
        response = self.function_with_return_json()
        assert user_dict_validate.validate(response)

    @patch('app.views.helper.request')
    def test_without_headers_get(self, mock_request):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()

    @patch('app.views.helper.jwt.decode', side_effect=Exception())
    @patch('app.views.helper.request')
    def test_failed_decode(self, mock_request, mock_decode):
        mock_request.headers.get.return_value = None
        with self.assertRaises(Unauthorized):
            self.function_without_return()

    @patch(
        'app.views.helper.jwt.decode',
        return_value={'access': 'common', 'id': 2}
    )
    @patch('app.views.helper.request')
    def test_not_admin_and_owner(self, mock_decode, mock_request):
        mock_request.headers.get.return_value = 'token'
        with self.assertRaises(Unauthorized):
            self.function_without_return()


class TestRequestJsonMustHave(unittest.TestCase):

    @request_json_must_have(['id', 'access'])
    def function(self):
        pass

    @patch('app.views.helper.request')
    def test_success(self, mock_request):
        mock_request.json = {'id': 1, 'access': 'access'}
        response = self.function()
        assert not response

    @patch('app.views.helper.request')
    def test_failed_exception(self, mock_request):
        mock_request.json = {'access': 'access'}
        with self.assertRaises(UnprocessableEntity):
            self.function()

        try:
            self.function()
        except Exception as e:
            message_test = (
                '422 Unprocessable Entity: Missing id '
                'or access into request body'
            )
            assert str(e) == message_test


class TestRequestJsonMustHaveOne(unittest.TestCase):

    @request_json_must_have_one(['id', 'access'])
    def function(self):
        pass

    @patch('app.views.helper.request')
    def test_success(self, mock_request):
        mock_request.json = {'id': 1}
        response = self.function()
        assert not response

    @patch('app.views.helper.request')
    def test_failed_exception(self, mock_request):
        mock_request.json = {}
        with self.assertRaises(UnprocessableEntity):
            self.function()

        try:
            self.function()
        except Exception as e:
            message_test = (
                '422 Unprocessable Entity: Missing id '
                'and access into request body'
            )
            assert str(e) == message_test
