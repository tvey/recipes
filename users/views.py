from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _

from .models import User
from .forms import RegistrationForm, LoginForm, EmailForm, ChangePasswordForm
from .tasks import send_email


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{timestamp}{user.is_active}'


token_generator = TokenGenerator()


def send_activation_link(request, user, first=True):
    """Сформировать ссылку и отправить письмо для активации аккаунта."""
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    mail_subject = _('Активация аккаунта')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    html_message = render_to_string(
        'users/registration_activation_email.html',
        {
            'user': user,
            'domain': current_site,
            'uidb64': uid,
            'token': token,
            'protocol': protocol,
            'first': first,
        },
    )
    plain_message = strip_tags(html_message)

    send_email.delay(
        user.email,
        subject=mail_subject,
        message=plain_message,
        html_message=html_message,
    )


def register(request):
    """Регистрация пользователя.

    Сохранить нового пользователя в бд со статусом is_active=False
    и отправить на почту ссылку активации аккаунта.
    """
    if request.user.is_authenticated:
        return redirect('recipes:home')

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_link(request, user)
            msg = _(
                'Добро пожаловать! Для завершения регистрации '
                'проверьте свою электронную почту.'
            )
            messages.success(request, msg)
            return redirect('users:login')
        elif User.objects.filter(email__iexact=email, is_active=False).exists():
            return render(request, 'users/registration_activation_error.html')

        return redirect(request.path_info)

    return render(request, 'users/auth.html', {'form': form})


def activate_account(request, uidb64, token):
    """Задать is_active=True, когда пользователь пройдёт по ссылке активации."""
    if request.user.is_authenticated:
        return redirect('recipes:home')

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        msg = _(
            'Отлично! Теперь можно войти на сайт, '
            'чтобы создавать, сохранять и делиться рецептами.'
        )
        messages.success(request, msg)
        return redirect('users:login')

    return render(request, 'users/registration_activation_error.html')


def resend_activation(request):
    """Отправить письмо с новой ссылкой активации."""
    if request.user.is_authenticated:
        messages.info(request, _('Ваш аккаунт уже активирован.'))
        return redirect('recipes:home')

    form = EmailForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email', None)
        try:
            user = User.objects.get(email__iexact=email)
            if user.is_active:
                msg = _('Аккаунт с такой почтой уже активирован.')
                messages.info(request, msg)
                return redirect('users:login')
            send_activation_link(request, user, first=False)
            messages.info(request, _('Новая ссылка отправлена, проверьте свою почту.'))
            return redirect('users:login')
        except User.DoesNotExist:
            msg = _('Пожалуйста, укажите тот адрес, с которым регистрировались.')
            messages.error(request, msg)
            return redirect(request.path_info)
    context = {'form': form}
    return render(request, 'users/registration_activation_resend.html', context)


class LoginUserView(LoginView):
    template_name = 'users/auth.html'
    redirect_authenticated_user = True
    form_class = LoginForm


@login_required
def change_password(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    old = request.POST.get('old_password')
    new = request.POST.get('new_password1')

    if form.is_valid():
        old = request.POST.get('old_password')
        new = request.POST.get('new_password1')
        if old == new:
            messages.info(request, _('Вы не изменили свой пароль.'))
        else:
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Пароль успешно изменён!'))
        return redirect('recipes:home')

    return render(request, 'users/password_change.html', {'form': form})
