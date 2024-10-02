import pytest
from pytest_factoryboy import register
from factories import UserFactory, LeaveFactory


register(UserFactory)
register(LeaveFactory)
