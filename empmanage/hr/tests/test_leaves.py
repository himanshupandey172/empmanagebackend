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
