from django.contrib.auth.views import LogoutView
from django.urls import reverse, resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.views import (
    register,
    LoginUserView,
    activate_account,
    resend_activation,
    change_password,
    token_generator,
)


def test_register_path_resolves_to_register_view():
    path = reverse('users:register')
    resolver = resolve(path)
    assert resolver.func == register
    assert resolver.url_name == 'register'
    assert resolver.namespace == 'users'
    assert resolver.route == 'join/'


def test_login_path_resolves_to_login_view():
    path = reverse('users:login')
    resolver = resolve(path)
    assert resolver.func.view_class == LoginUserView
    assert resolver.url_name == 'login'
    assert resolver.namespace == 'users'
    assert resolver.route == 'login/'


def test_logout_path_resolves_logout_view():
    path = reverse('users:logout')
    resolver = resolve(path)
    assert resolver.func.view_class == LogoutView
    assert resolver.url_name == 'logout'
    assert resolver.namespace == 'users'
    assert resolver.route == 'logout/'


def test_activate_account_path_resolves_to_activate_account_view(new_user):
    user = new_user()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    params = {'uidb64': uid, 'token': token}
    path = reverse('users:activate-account', kwargs=params)
    resolver = resolve(path)
    assert resolver.func == activate_account
    assert resolver.url_name == 'activate-account'
    assert resolver.namespace == 'users'
    assert resolver.route == 'activate/<uidb64>/<token>/'


def test_resend_activation_resolves():
    path = reverse('users:resend-activation')
    resolver = resolve(path)
    assert resolver.func == resend_activation
    assert resolver.url_name == 'resend-activation'
    assert resolver.namespace == 'users'
    assert resolver.route == 'resend-activation/'


def test_change_password_resolves():
    path = reverse('users:change-password')
    resolver = resolve(path)
    assert resolver.func == change_password
    assert resolver.url_name == 'change-password'
    assert resolver.namespace == 'users'
    assert resolver.route == 'change-password/'
