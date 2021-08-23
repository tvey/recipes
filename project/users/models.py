from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'({self.username}, {self.email})'


# additional user fields: photo, some preferences
# also handle relationships - subscriptions


# форма для юзера + форма профиля


# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     display_name = models.CharField(max_length=100, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.display_name:
#             if self.user.first_name and self.user.last_name:
#                 self.display_name = (
#                     f'{self.user.first_name} {self.user.last_name}'
#                 )
#             elif selfuser.first_name:
#                 self.display_name = self.user.first_name
#             else:
#                 self.display_name = self.user.username
#         super().save(*args, **kwargs)
