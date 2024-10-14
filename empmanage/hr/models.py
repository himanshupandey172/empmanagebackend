from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms import ValidationError

# Create your models here.


class Employee(models.Model):
    # Define some constants for the department codes
    RND = "R&D"
    ENG = "ENG"
    MKT = "MKT"
    SAL = "SAL"
    OPS = "OPS"

    # Define a list of tuples for the department choices
    department_choices = [
        (RND, "Research and Development"),
        (ENG, "Engineering"),
        (MKT, "Marketing"),
        (SAL, "Sales"),
        (OPS, "Operations"),
    ]

    RND_LEAD = "R&D Lead"
    RND_ENG = "R&D Engineer"
    RND_ML = "Machine Learning Engineer"
    RND_AI = "Artificial Intelligence Engineer"
    RND_ROB = "Robotics Engineer"

    ENG_LEAD = "Engineering Lead"
    ENG_DEV = "Software Developer"
    ENG_QA = "Quality Assurance Engineer"
    ENG_NET = "Network Engineer"
    ENG_HW = "Hardware Engineer"

    MKT_LEAD = "Marketing Lead"
    MKT_MGR = "Marketing Manager"
    MKT_ANA = "Marketing Analyst"
    MKT_SEO = "SEO Specialist"
    MKT_SMM = "Social Media Manager"

    SAL_LEAD = "Sales Lead"
    SAL_MGR = "Sales Manager"
    SAL_REP = "Sales Representative"
    SAL_CON = "Sales Consultant"
    SAL_SUP = "Sales Support"

    OPS_LEAD = "Operations Lead"
    OPS_MGR = "Operations Manager"
    OPS_ADM = "Operations Administrator"
    OPS_TEC = "Operations Technician"
    OPS_SUP = "Operations Support"

    # Define a list of tuples for the employee designations choices
    # Note: the first element of each tuple is a combination of the department code and the designation code
    designation_choices = [
        (RND + "_" + RND_LEAD, "Research and Development Lead"),
        (RND + "_" + RND_ENG, "Research and Development Engineer"),
        (RND + "_" + RND_ML, "Machine Learning Engineer"),
        (RND + "_" + RND_AI, "Artificial Intelligence Engineer"),
        (RND + "_" + RND_ROB, "Robotics Engineer"),
        (ENG + "_" + ENG_LEAD, "Engineering Lead"),
        (ENG + "_" + ENG_DEV, "Software Developer"),
        (ENG + "_" + ENG_QA, "Quality Assurance Engineer"),
        (ENG + "_" + ENG_NET, "Network Engineer"),
        (ENG + "_" + ENG_HW, "Hardware Engineer"),
        (MKT + "_" + MKT_LEAD, "Marketing Lead"),
        (MKT + "_" + MKT_MGR, "Marketing Manager"),
        (MKT + "_" + MKT_ANA, "Marketing Analyst"),
        (MKT + "_" + MKT_SEO, "SEO Specialist"),
        (MKT + "_" + MKT_SMM, "Social Media Manager"),
        (SAL + "_" + SAL_LEAD, "Sales Lead"),
        (SAL + "_" + SAL_MGR, "Sales Manager"),
        (SAL + "_" + SAL_REP, "Sales Representative"),
        (SAL + "_" + SAL_CON, "Sales Consultant"),
        (SAL + "_" + SAL_SUP, "Sales Support"),
        (OPS + "_" + OPS_LEAD, "Operations Lead"),
        (OPS + "_" + OPS_MGR, "Operations Manager"),
        (OPS + "_" + OPS_ADM, "Operations Administrator"),
        (OPS + "_" + OPS_TEC, "Operations Technician"),
        (OPS + "_" + OPS_SUP, "Operations Support"),
    ]

    # Define a CharField for the employee designation with the choices argument
    designation = models.CharField(
        max_length=50,
        choices=designation_choices,
        blank=True,
        default=RND + "_" + RND_LEAD,
    )

    # Define a CharField for the department with the choices argument
    department = models.CharField(
        max_length=16, choices=department_choices, blank=True, default=RND
    )
    phone = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    readonly_fields = ("total_cl", "total_el", "total_sl")

    total_cl = models.PositiveIntegerField(
        default=7, validators=[MinValueValidator(0), MaxValueValidator(7)]
    )

    total_sl = models.PositiveIntegerField(
        default=7, validators=[MinValueValidator(0), MaxValueValidator(7)]
    )

    total_el = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(13)]
    )

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        ordering = ["user__first_name", "user__last_name"]


class EmployeeAttendance(models.Model):
    ON_LEAVE = "L"
    PRESENT = "P"
    HALF_DAY = "H"

    attendance_choices = [
        (ON_LEAVE, "On Leave"),
        (PRESENT, "Present"),
        (HALF_DAY, "Half Day"),
    ]

    attendance = models.CharField(
        max_length=16, choices=attendance_choices, blank=True, default=PRESENT
    )

    OFFICE = "OFFICE"
    SITE = "SITE"
    WORK_FROM_HOME = "WFH"

    location_choices = [
        (OFFICE, "In Office"),
        (SITE, "On Site"),
        (WORK_FROM_HOME, "Work from Home"),
    ]

    location = models.CharField(
        max_length=16, choices=location_choices, blank=True, default=None
    )

    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    activity_description = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class EmployeeLeave(models.Model):
    CASUAL_LEAVE = "CL"
    EARNED_LEAVE = "EL"
    SICK_LEAVE = "SL"

    leave_choices = [
        (CASUAL_LEAVE, "Casual Leave"),
        (EARNED_LEAVE, "Earned Leave"),
        (SICK_LEAVE, "Sick Leave"),
    ]

    leave = models.CharField(
        max_length=16,
        choices=leave_choices,
        default=CASUAL_LEAVE,
    )

    leave_reason = models.TextField(null=True, blank=True)
    leave_from = models.DateTimeField(null=True, blank=True)
    leave_to = models.DateTimeField(null=True, blank=True)
    total_days = models.PositiveIntegerField(default=0)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        leave_types = {"CL": "total_cl", "SL": "total_sl", "EL": "total_el"}
        employee = self.employee
        field = leave_types[self.leave]
        balance = getattr(employee, field)

        # Increment the leave balance when the leave record is deleted
        setattr(employee, field, balance + self.total_days)
        employee.save()

        # Call the original delete method to handle the actual deletion
        super(EmployeeLeave, self).delete(*args, **kwargs)


class EmployeeExpense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()


class EmployeeTimesheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    task_description = models.TextField()


# Sick Leave=7 leaves (Jan-dec)
# Casual Leaves =7 Leaves (Jan-dec)
# (Become zero at every start of new year)(No carry forward)

# Earned leave= after every 30 continues working days, 1 earn leave will be added and which will be paid if employee not consumed that..
