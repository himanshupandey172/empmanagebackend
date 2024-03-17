from django.urls import include, path
from . import views

# from rest_framework_nested import routers  Will use when need nested routes
from pprint import pprint

from rest_framework import routers


router = routers.DefaultRouter()
router.register("employees", views.EmployeeViewSet)
router.register("attendance", views.EmployeeAttendanceViewSet, basename="attendance")
router.register("leaves", views.EmployeeLeaveViewSet, basename="leaves")

urlpatterns = router.urls
# pprint(router.urls)
