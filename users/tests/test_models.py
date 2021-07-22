import pytest

from django.db import IntegrityError


def test_user_username_field(new_user):
    user = new_user()
    assert user.USERNAME_FIELD == 'username'


def test_email_field_required(new_user):
    user = new_user()
    assert 'email' in user.REQUIRED_FIELDS


def test_user_has_default_fields(new_user):
    user = new_user()
    assert hasattr(user, 'first_name')
    assert hasattr(user, 'last_name')
    assert hasattr(user, 'is_active')
    assert hasattr(user, 'date_joined')


@pytest.mark.django_db
def test_email_field_unqie(django_user_model, new_user, email_fix):
    new_user(email=email_fix)

    with pytest.raises(IntegrityError):
        new_user(email=email_fix)
