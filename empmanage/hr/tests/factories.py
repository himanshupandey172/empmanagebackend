import factory
from faker import Faker
from core.models import User
from hr.models import Employee, EmployeeLeave

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: fake.unique.name())
    email = factory.LazyAttribute(lambda x: fake.unique.email())


# class EmployeeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Employee


class LeaveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeLeave
