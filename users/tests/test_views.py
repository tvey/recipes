import pytest

from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.views import (
    register,
    activate_account,
    resend_activation,
    LoginUserView,
    change_password,
    token_generator,
)

register_path = reverse('users:register')
login_path = reverse('users:login')
homepage = reverse('recipes:home')
anonymous_user = AnonymousUser()


def activate_path(user):
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    params = {'uidb64': uid, 'token': token}
    path = reverse('users:activate-account', kwargs=params)
    return path


def test_register_view_is_ok(client):
    response = client.get(register_path)
    assert response.status_code == 200


def test_register_view_redirects_authenticated_user(client, new_user):
    client.force_login(new_user())
    response = client.get(register_path)
    assert response.status_code == 302
    assert response.url == homepage


# To-do
# def test_register_inactive_user_redirects_to_error_page(
#     rf, client, new_inactive_user
# ):
#     pass


# To-do
# def test_register_view_creates_inactive_user(
#     client, username_fix, email_fix, password_fix, django_user_model
# ):
#     data = {
#         'email': email_fix,
#         'username': username_fix,
#         'password1': password_fix,
#         'password2': password_fix,
#     }
#     response = client.post(register_path, **data)
#     user_exists = django_user_model.objects.get(username=username_fix).exists()
#     assert user_exists


def test_activate_account_view_redirects_authenticated_user(client, new_user):
    user = new_user()
    path = activate_path(user)
    client.force_login(user)
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == homepage


# To-do
# def test_registration_activation_email_sent(client, new_user):
#     pass


# To-do
# def test_activation_link_generation():
#     # check if email content is with generated - token/uuid
#     pass


# To-do
# def test_activated_user_redirected_to_login_page():
#   pass


# To-do
# def test_resend_activation():
#   pass


# To-do
# def test_resend_activation_user_does_not_exist():
#   pass


def test_login_view_is_ok(client):
    response = client.get(login_path)
    assert response.status_code == 200


def test_login_view_redirect_authenticated_user(client, new_user):
    client.force_login(new_user())
    response = client.get(login_path)
    assert response.status_code == 302
    assert response.url == homepage


def test_login_active_user_with_username(client, new_user, password_fix):
    user = new_user(password=password_fix)
    logged_in = client.login(username=user.username, password=password_fix)
    assert logged_in


def test_login_active_user_with_email(client, new_user, password_fix):
    user = new_user(password=password_fix)
    logged_in = client.login(username=user.email, password=password_fix)
    assert logged_in


# To-do
# def test_login_inactive_user(rf, client, new_inactive_user, password_fix):
#     user = new_inactive_user(password=password_fix)
#     request = rf.get(login_path)
#     request.user = user

#     assert False


def test_logout_view(client, new_user):
    path = reverse('users:logout')
    client.force_login(new_user())
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == homepage


def test_logout_view_redirect_anonymous_user(client):
    path = reverse('users:logout')
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == homepage


def test_change_password_view_redirects_anonymous_user(client):
    path = reverse('users:change-password')
    response = client.get(path)
    assert response.status_code == 302
    assert 'login' in response.url
    assert 'next' in response.url
    assert 'change-password' in response.url


# To-do
# def test_change_password_view(client, new_user, password_fix):
#     path = reverse('users:change-password')
#     user = new_user(password=password_fix)
#     old_hash = user.password
#     new_password = password_fix + '123'
#     client.force_login(user)
#     data = {
#         'old_password': password_fix,
#         'new_password1': new_password,
#         'new_password2': new_password,
#     }
#     response = client.post(path, **data)
#     template_names = [t.name for t in response.templates]
#     assert response.status_code == 200
#     assert 'Изменить пароль' in response.content.decode('utf-8')
#     assert 'users/password_change.html' in template_names
#     assert old_hash != user.password
