# from app.views.helper import token_owner_or_admin_required
# from werkzeug.exceptions import NotFound, Unauthorized
# from app.views.user import is_admin
# from mock import call
# import pytest


# @token_owner_or_admin_required(user='kasf')
# def interal_function():
#     return "Batata"


# def test_is_admin_success(mocker):
#     id = 12351841
#     mocker_is_admin = mocker.patch(
#         'app.views.user.find_by_id', return_value={'admin': True}
#     )
#     response = is_admin(id)
#     assert mocker_is_admin.called
#     assert mocker_is_admin.call_args == call(id)
#     assert response


# @pytest.mark.parametrize(
#     "expected_return_value, id",
#     [(None, 123), ({}, 321)]
# )
# def test_is_admin_Failed(mocker, expected_return_value, id):
#     mocker_is_admin = mocker.patch(
#         'app.views.user.find_by_id',
#         return_value=expected_return_value
#     )
#     assert mocker_is_admin.return_value == expected_return_value
#     with pytest.raises(NotFound):
#         is_admin(id)
#     assert mocker_is_admin.called
#     assert mocker_is_admin.call_args == call(id)


# def test_token_owner_or_admin_required(mocker):
#     mocker_request = mocker.patch('app.views.helper.request')
#     mocker_request.headers.get.return_value = None

#     @token_owner_or_admin_required()
#     def interal_function():
#         return "Batata"

#     with pytest.raises(Unauthorized):
#         interal_function()
#     pass
