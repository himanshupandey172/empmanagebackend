from django.shortcuts import render
from django.http import HttpResponse
from hr.models import Employee, EmployeeAttendance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import pprint
from rest_framework.viewsets import ModelViewSet

# Create your views here.


# To get EmployeeAttendance of current employee
# query_attendance = EmployeeAttendance.objects.select_related("employee").filter(
#         employee__id=employee.id
#     )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def say_hello(request):
    employee = Employee.objects.select_related("user").get(user__id=request.user.id)
    queryset = Employee.objects.select_related("user").all()
    my_attendance = EmployeeAttendance(pk=19)
    my_attendance.delete()

    query_attendance = EmployeeAttendance.objects.select_related("employee").filter(
        employee__id=employee.id
    )

    return render(
        request,
        "hello.html",
        {"name": "Himanshu", "employees": list(query_attendance)},
    )


class TestViewSet(ModelViewSet):
    pass
