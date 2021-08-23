import pytest

from users.backends import EmailOrUsernameModelBackend

backend = EmailOrUsernameModelBackend()


@pytest.mark.django_db
def test_authenticate_with_username(rf, new_user, password_fix):
    user = new_user(password=password_fix)
    request = rf.get('/')
    data = {'username': user.username, 'password': password_fix}
    result = backend.authenticate(request, **data)
    assert result == user


@pytest.mark.django_db
def test_authenticate_with_email(rf, new_user, password_fix):
    user = new_user(password=password_fix)
    request = rf.get('/')
    data = {'username': user.email, 'password': password_fix}
    result = backend.authenticate(request, **data)
    assert result == user


@pytest.mark.django_db
def test_authenticate_with_wrong_password(rf, new_user, password_fix):
    request = rf.get('/')
    data = {'username': new_user().username, 'password': password_fix}
    result = backend.authenticate(request, **data)
    assert result is None


@pytest.mark.django_db
def test_authenticate_user_does_not_exist(rf, username_fix, password_fix):
    request = rf.get('/')
    data = {'username': username_fix, 'password': password_fix}
    result = backend.authenticate(request, **data)
    assert result is None


@pytest.mark.django_db
def test_authenticate_returns_none(rf):
    request = rf.get('/')
    result = backend.authenticate(request)
    assert result is None
