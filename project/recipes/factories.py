import factory
from faker import Faker

# from recipes.models import Recipe

fake = Faker('ru_RU')


# class RecipeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Recipe

#     username = fake.user_name()
#     email = fake.email()
#     password = factory.PostGenerationMethodCall('set_password', fake.password())
#     is_active = True
