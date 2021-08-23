from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    register,
    activate_account,
    resend_activation,
    LoginUserView,
    change_password,
)

app_name = 'users'

urlpatterns = [
    path('join/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate-account'),
    path('resend-activation/', resend_activation, name='resend-activation'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', change_password, name='change-password'),
]
