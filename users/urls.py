from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
)


from .views import (
    register,
    LoginUserView,
)

app_name = 'users'

urlpatterns = [
    path('join/', register, name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
