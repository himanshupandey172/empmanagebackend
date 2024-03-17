# from rest_framework.test import APIClient
# from rest_framework import status
# import pytest

# from core.serializers import UserCreateSerializer
# from core.models import User
# from hr.models import Employee, EmployeeLeave
# from hr.serializers import EmployeeLeaveSerializer, CreateEmployeeLeaveSerializer


# @pytest.mark.django_db
# class TestGetLeaves:
#     @pytest.mark.skip(reason="this test is not needed anymore")
#     def test_if_user_is_anonymous_returns_401(self):
#         client = APIClient()
#         response = client.get("/hr/leaves/")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     @pytest.mark.django_db(transaction=True)
#     def test_create_leave_admin_user_201(
#         self,
#         get_user_credentials,
#         create_user,
#         get_user_access_token,
#         get_user_leave_object,
#     ):

#         admin_leave_object = {
#             # "employee_id": 1,
#             "leave": "SL",
#             "leave_reason": "",
#             "leave_from": "",
#             "leave_to": "",
#             "total_days": 1,
#         }

#         # (admin_leave_object) = get_user_leave_object
#         (admin_access_token) = get_user_access_token

#         client = APIClient()
#         response = client.post(
#             "/hr/leaves/",
#             admin_leave_object,
#             HTTP_AUTHORIZATION=f"JWT {admin_access_token}",
#         )
#         print(response.data)
#         assert response.status_code == 201
#         self.validate_response_data(response.data)

#     def validate_response_data(self, data):
#         serializer = CreateEmployeeLeaveSerializer(data=data)
#         serializer.is_valid()
#         print(serializer.data["leave"])
#         assert serializer.is_valid(), serializer.data["leave"] == "CL"

# def test_get_all_leaves(
#     get_user_credentials,
#     create_user,
#     get_user_access_token,
#     get_user_leave_object,
# ):
#     (admin_access_token) = get_user_access_token
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"JWT {admin_access_token}")
#     response = client.get("/hr/leaves/")
#     print(response.data["results"])
#     assert response.status_code == 200
# {
#     "employee_id": 1,
#     "leave": "SL",
#     "leave_reason": "",
#     "leave_from": "",
#     "leave_to": "",
#     "total_days": 1,
# }


# def test_new_user(user_factory):
#     print(user_factory.username)
#     assert True

import pytest
from hr.models import Employee, EmployeeLeave
from hr.serializers import CreateEmployeeLeaveSerializer
from rest_framework.test import APIClient


@pytest.mark.django_db
@pytest.mark.skip
def test_leave_deduction(user_factory):
    client = APIClient()

    authenticated_user = user_factory()
    authenticated_employee = Employee.objects.get(user=authenticated_user)

    client.force_authenticate(user=authenticated_user)

    initial_cl = authenticated_employee.total_cl

    leave_data = {
        "leave": "CL",
        "total_days": 1,
    }

    response = client.post("/hr/leaves/", leave_data, format="json")

    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code}"

    authenticated_employee.refresh_from_db()

    expected_cl = initial_cl - leave_data["total_days"]
    assert (
        authenticated_employee.total_cl == expected_cl
    ), f"Expected total_cl to be {expected_cl}, but got {authenticated_employee.total_cl}"


@pytest.mark.django_db
def test_admin_can_view_all_leaves(user_factory, leave_factory):
    client = APIClient()
    # Create regular users and associated leaves
    for _ in range(3):
        user = user_factory()
        leave_factory(employee__user=user)

    # Create an admin user
    admin_user = user_factory(is_staff=True, is_superuser=True)

    # Authenticate as the admin user
    client.force_authenticate(user=admin_user)

    # Make a GET request to the leaves endpoint
    response = client.get("/hr/leaves/")

    # Verify that the admin user can see all leaves
    assert response.status_code == 200
    assert len(response.data) == 3, "Admin should be able to see all leaves"
