import pytest
from pytest_factoryboy import register
from faker import Faker

from .factories import UserFactory

from users.utils import rand_locale

fake = Faker(rand_locale)

register(UserFactory)


@pytest.fixture
def email_fix():
    return fake.email()


@pytest.fixture
def password_fix():
    return fake.password()


@pytest.fixture
def short_text():
    return fake.sentence()


@pytest.fixture
def long_text():
    return fake.text()


@pytest.fixture
def new_user(db, user_factory):
    return user_factory.create()


@pytest.fixture
def new_inactive_user(db, user_factory):
    return user_factory.create(is_active=False)
