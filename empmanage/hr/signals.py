from .models import Employee, EmployeeLeave
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Employee.objects.create(user=kwargs["instance"])


@receiver(post_delete, sender=EmployeeLeave)
def update_leave_balance(sender, instance, **kwargs):
    employee = instance.employee
    leave_type = instance.leave
    leave_types = {"CL": "total_cl", "SL": "total_sl", "EL": "total_el"}
    field = leave_types[leave_type]
    current_balance = getattr(employee, field)
    setattr(employee, field, current_balance + instance.total_days)
    employee.save()
