# from rest_framework.test import APIClient
# from rest_framework import status
# import pytest


# # Arrange Act Assert


# @pytest.mark.django_db
# class TestLogin:
#     def test_employee_enter_invalid_username_returns_401(self):
#         client = APIClient()
#         response = client.post(
#             "/auth/jwt/create/", {"username": "invalid", "password": "ILoveDjango"}
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_employee_enter_invalid_password_returns_401(self):
#         client = APIClient()
#         response = client.post(
#             "/auth/jwt/create/", {"username": "test@gmail.com", "password": "invalid"}
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_employee_enter_valid_username_valid_password_returns_200(self):
#         client = APIClient()
#         response = client.post(
#             "/auth/jwt/create/", {"username": "admin", "password": "admin"}
#         )
#         print(f"logs {client.__dict__}")
#         assert response.status_code == status.HTTP_200_OK


# /hr/leaves/
# GET operation
# if admin --> get all employee leaves
# if authenticated employee --> get only this employee leave
# if unauthenticated user --> 401 unauthorized

# POST operation
# if admin --> create all employee leaves
# if authenticated employee --> create only this employee leave
# if unauthenticated user --> 401 unauthorized


# PATCH operation
# if admin --> update all employee leaves
# if authenticated employee --> 403 forbidden
# if unauthenticated user --> 401 unauthorized


# Import the necessary modules
# Import the necessary modules
# import pytest
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User
# from hr.models import EmployeeLeave


# # Create a fixture for the API client
# @pytest.fixture
# def api_client():
#     return APIClient()


# # Create a fixture to get a valid JWT token for a user or an API client
# @pytest.fixture
# def get_jwt_token(api_client, username, password):
#     # Make a POST request to the /auth/jwt/create/ endpoint with the username and password
#     response = api_client.post(
#         "/auth/jwt/create/", {"username": username, "password": password}
#     )
#     # Return the access token from the response
#     return response.data["access"]


# # Create a fixture to create some sample data for the EmployeeLeave model
# @pytest.fixture
# def create_leaves(db):
#     # Create some employees
#     emp1 = User.objects.create(username="emp1", password="emp1")
#     emp2 = User.objects.create(username="emp2", password="emp2")
#     emp3 = User.objects.create(username="emp3", password="emp3")
#     # Create some leaves
#     leave1 = EmployeeLeave.objects.create(
#         leave="CL",
#         leave_reason="Vacation",
#         leave_from="2024-02-01",
#         leave_to="2024-02-05",
#         total_days=5,
#         employee=emp1,
#     )
#     leave2 = EmployeeLeave.objects.create(
#         leave="EL",
#         leave_reason="Personal",
#         leave_from="2024-02-10",
#         leave_to="2024-02-15",
#         total_days=6,
#         employee=emp2,
#     )
#     leave3 = EmployeeLeave.objects.create(
#         leave="SL",
#         leave_reason="Sick",
#         leave_from="2024-02-20",
#         leave_to="2024-02-22",
#         total_days=3,
#         employee=emp3,
#     )
#     return [leave1, leave2, leave3]


# # Use the parametrize marker to run the same test with different values and scenarios
# @pytest.mark.parametrize(
#     "username, password, status_code, expected_data",
#     [
#         # Test case 1: if admin, get all employee leaves
#         (
#             "admin",
#             "admin",
#             200,
#             [
#                 {
#                     "leave": "CL",
#                     "leave_reason": "Vacation",
#                     "leave_from": "2024-02-01",
#                     "leave_to": "2024-02-05",
#                     "total_days": 5,
#                     "employee": 1,
#                 },
#                 {
#                     "leave": "EL",
#                     "leave_reason": "Personal",
#                     "leave_from": "2024-02-10",
#                     "leave_to": "2024-02-15",
#                     "total_days": 6,
#                     "employee": 2,
#                 },
#                 {
#                     "leave": "SL",
#                     "leave_reason": "Sick",
#                     "leave_from": "2024-02-20",
#                     "leave_to": "2024-02-22",
#                     "total_days": 3,
#                     "employee": 3,
#                 },
#             ],
#         ),
#         # Test case 2: if authenticated employee, get only this employee leave
#         (
#             "emp1",
#             "emp1",
#             200,
#             [
#                 {
#                     "leave": "CL",
#                     "leave_reason": "Vacation",
#                     "leave_from": "2024-02-01",
#                     "leave_to": "2024-02-05",
#                     "total_days": 5,
#                     "employee": 1,
#                 }
#             ],
#         ),
#         # Test case 3: if unauthenticated user, 401 unauthorized
#         (None, None, 401, {"detail": "Authentication credentials were not provided."}),
#     ],
# )
# # Define the test function
# def test_get_leaves(
#     api_client,
#     get_jwt_token,
#     create_leaves,
#     username,
#     password,
#     status_code,
#     expected_data,
# ):
#     # Get a valid JWT token for the user or the API client
#     if username and password:
#         token = get_jwt_token(username, password)
#         # Set the authentication header
#         api_client.credentials(HTTP_AUTHORIZATION=f"JWT {token}")
#     # Make a GET request to the /hr/leaves/ endpoint
#     response = api_client.get("/hr/leaves/")
#     # Assert that the status code is as expected
#     assert response.status_code == status_code
#     # Assert that the response data is as expected
#     assert response.data == expected_data
