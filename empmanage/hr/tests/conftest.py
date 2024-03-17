# import pytest
# from core.models import User
# from rest_framework.test import APIClient


# @pytest.fixture
# def get_user_credentials():
#     admin_user_credentials = {
#         "username": "adminuser",
#         "password": "ILoveDjango",
#         "email": "admin@lemon.com",
#         "is_staff": True,
#         "total_cl": 7,
#         "total_sl": 0,
#     }

#     return admin_user_credentials


# @pytest.fixture
# def create_user(db, get_user_credentials):
#     (admin_user_credentials) = get_user_credentials
#     client = APIClient()
#     admin_user = client.post("/auth/users/", admin_user_credentials)
#     return admin_user


# @pytest.fixture
# def get_user_access_token(get_user_credentials):
#     client = APIClient()
#     (admin_user_credentials) = get_user_credentials
#     admin_token_response = client.post(
#         "/auth/jwt/create",
#         {
#             "username": admin_user_credentials["username"],
#             "password": admin_user_credentials["password"],
#         },
#     )
#     admin_access_token = admin_token_response.data["access"]
#     return admin_access_token


# @pytest.fixture
# def get_user_leave_object():
#     admin_leave_object = {"leave": "SL", "leave_reason": "vacation", "total_days": 1}
#     return admin_leave_object


import pytest
from pytest_factoryboy import register
from factories import UserFactory, LeaveFactory


register(UserFactory)
register(LeaveFactory)
