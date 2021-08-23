from faker import Faker
import factory

from users.models import User
from users.utils import rand_locale

fake = Faker(rand_locale)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.user_name()
    email = fake.email()
    password = factory.PostGenerationMethodCall('set_password', fake.password())
    is_active = True
