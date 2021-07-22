import pytest

from users.forms import (
    RegistrationForm,
    LoginForm,
    EmailForm,
    ResetPasswordForm,
    ChangePasswordForm,
    SetUserPasswordForm,
)


@pytest.mark.django_db
def test_registration_form_is_valid(email_fix, username_fix, password_fix):
    form = RegistrationForm(
        data={
            'email': email_fix,
            'username': username_fix,
            'password1': password_fix,
            'password2': password_fix,
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_registration_form_passwords_do_not_match(
    email_fix, username_fix, password_fix
):
    form = RegistrationForm(
        data={
            'email': email_fix,
            'username': username_fix,
            'password1': password_fix,
            'password2': password_fix + 'blah',
        }
    )
    assert not form.is_valid()
    assert 'пароли не совпадают' in str(form.errors)


@pytest.mark.django_db
def test_registration_form_with_bad_email(email_fix, username_fix, password_fix):
    form = RegistrationForm(
        data={
            'email': username_fix,
            'username': username_fix,
            'password1': password_fix,
            'password2': password_fix,
        }
    )
    assert not form.is_valid()
    assert 'правильный адрес электронной почты' in str(form.errors)


@pytest.mark.django_db
def test_registration_form_with_bad_username(email_fix, username_fix, password_fix):
    form = RegistrationForm(
        data={
            'username': username_fix + '!!!',
            'password1': password_fix,
            'password2': password_fix,
        }
    )
    assert not form.is_valid()
    assert 'только разрешённые символы' in str(form.errors)


@pytest.mark.django_db
def test_registration_form_no_email(username_fix, password_fix):
    form = RegistrationForm(
        data={
            'username': username_fix,
            'password1': password_fix,
            'password2': password_fix,
        }
    )
    assert not form.is_valid()
    assert 'Обязательное поле' in str(form.errors)

@pytest.mark.django_db
def test_registration_form_no_username(email_fix, password_fix):
    form = RegistrationForm(
        data={
            'email': email_fix,
            'password1': password_fix,
            'password2': password_fix,
        }
    )
    assert not form.is_valid()
    assert 'Обязательное поле' in str(form.errors)


def test_login_form_is_valid(new_user, password_fix):
    raw_password = password_fix
    user = new_user(password=raw_password)
    form = LoginForm(data={'username': user.username, 'password': raw_password})
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_is_not_valid(email_fix, password_fix):
    form = LoginForm(data={'username': email_fix, 'password': password_fix})
    assert not form.is_valid()


def test_login_form_with_inactive_user_data_is_not_valid(
    new_inactive_user, password_fix
):
    raw_password = password_fix
    user = new_inactive_user(password=password_fix)
    form = LoginForm(data={'username': user.email, 'password': raw_password})
    assert not form.is_valid()
    assert 'аккаунт не активирован' in str(form.errors)


def test_email_form_with_invalid_email(username_fix):
    form = EmailForm(data={'email': username_fix})
    assert not form.is_valid()
    assert 'правильный адрес электронной почты' in str(form.errors)


def test_reset_password_form(new_user):
    form = ResetPasswordForm(data={'email': new_user().email})
    assert form.is_valid()


def test_reset_password_form_with_invalid_email(username_fix):
    form = ResetPasswordForm(data={'email': username_fix})
    assert not form.is_valid()
    assert 'правильный адрес электронной почты' in str(form.errors)


def test_change_password_form_is_valid(new_user, password_fix):
    old_password = password_fix
    new_password = old_password + '123'
    user = new_user(password=old_password)
    form = ChangePasswordForm(
        user,
        data={
            'old_password': old_password,
            'new_password1': new_password,
            'new_password2': new_password,
        },
    )
    assert form.is_valid()


def test_change_password_form_no_user_argument(password_fix):
    with pytest.raises(TypeError):
        form = ChangePasswordForm(
            data={
                'old_password': password_fix,
                'new_password1': password_fix,
                'new_password2': password_fix,
            },
        )


def test_change_password_form_passwords_do_not_match(new_user, password_fix):
    user = new_user(password=password_fix)
    form = ChangePasswordForm(
        user,
        data={
            'old_password': password_fix,
            'new_password1': password_fix + '123',
            'new_password2': password_fix + '456',
        },
    )
    assert not form.is_valid()
    assert 'пароли не совпадают' in str(form.errors)


def test_set_user_password_form_is_valid(new_user, password_fix):
    form = SetUserPasswordForm(
        new_user(), data={'new_password1': password_fix, 'new_password2': password_fix}
    )
    assert form.is_valid()


def test_set_user_password_form_no_user_argument(password_fix):
    with pytest.raises(TypeError):
        form = SetUserPasswordForm(
            data={'new_password1': password_fix, 'new_password2': password_fix}
        )


def test_set_user_password_form_passwords_do_not_match(new_user, password_fix):
    form = SetUserPasswordForm(
        new_user(),
        data={'new_password1': password_fix, 'new_password2': password_fix + '1'},
    )
    assert not form.is_valid()
    assert 'пароли не совпадают' in str(form.errors)
