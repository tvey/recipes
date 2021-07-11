from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .models import User
from .forms import RegistrationForm, LoginForm


def register(request):
    if request.user.is_authenticated:
        return redirect('recipes:home')

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        msg = 'Добро пожаловать!'
        messages.info(request, msg)
        return redirect('users:login')

    return render(request, 'users/auth.html', {'form': form})


class LoginUserView(LoginView):
    template_name = 'users/auth.html'
    redirect_authenticated_user = True
    form_class = LoginForm
