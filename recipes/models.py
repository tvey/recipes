from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from .utils import translit, generate_code

User = get_user_model()


class Category(models.Model):
    """Обширная категория рецепта: завтраки, салаты, выпечка и прочие."""

    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField(
        'Изображение', upload_to='recipe_images/content/', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Блюдо (подкатегория): каши, оливье, печенье."""

    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(
        'Изображение', upload_to='recipe_images/content/', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    """Кухня: европейская, французская, японская и т. д."""

    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField(
        'Изображение', upload_to='recipe_images/content/', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухни'

    def __str__(self):
        return self.name


class Diet(models.Model):
    """Тип питания: веган, палео, при диабете и прочие."""

    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField(
        'Изображение', upload_to='recipe_images/content/', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Тип питания'
        verbose_name_plural = 'Типы питания'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField('Название', max_length=150)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='Автор'
    )
    total_cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления', blank=True, null=True
    )
    difficulty = models.PositiveSmallIntegerField(
        'Сложность',
        choices=[
            (0, 'Легко'),
            (1, 'Средне'),
            (2, 'Сложно'),
        ],
    )
    description = models.TextField('Описание', blank=True, null=True)
    created = models.DateTimeField('Создан', default=timezone.now)
    updated = models.DateTimeField('Изменён', default=timezone.now)
    is_published = models.BooleanField('Опубликован', default=False)
    is_draft = models.BooleanField('Черновик', default=True)
    main_image = models.ImageField(
        'Основное фото',
        default='default.jpg',
        upload_to='recipe_images/%Y/%m/%d/',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    dishes = models.ManyToManyField(Dish, blank=True, verbose_name='Блюда')
    cuisines = models.ManyToManyField(Cuisine, blank=True, verbose_name='Кухни')
    diets = models.ManyToManyField(
        Diet, blank=True, verbose_name='Типы питания'
    )
    slug = models.SlugField(max_length=60, blank=True, null=True)
    shortcode = models.SlugField(max_length=10, blank=True, null=True)
    note = models.TextField('Примечание', blank=True, null=True)

    def __str__(self):
        return f'Рецепт {self.id}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        self.slug = translit(self.title)[:60]

        if not self.shortcode:
            self.shortcode = generate_code()
        super().save(*args, **kwargs)


class RecipeStep(models.Model):
    """Шаг (этап) приготовления."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image = models.ImageField(
        'Фото шага', upload_to='recipe_images/%Y/%m/%d/', blank=True, null=True
    )
    directions = models.TextField('Описание шага')

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'


class Product(models.Model):
    """Продукт, выбор из заранее заполненных данных."""

    name = models.CharField(max_length=100, unique=True)
    # nutritional facts pending

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Measure(models.Model):
    """Ед. измерения: шт. (штука), л (литр), ст. л. (столовая ложка) и т. д."""

    full_name = models.CharField('Полное название', max_length=50, unique=True)
    short_name = models.CharField(
        'Сокращённое название',
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class IngredientGroup(models.Model):
    """Группа индредиентов, например, тесто и начинка, коржи и крем."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа ингредиентов'
        verbose_name_plural = 'Группы ингредиентов'


class Ingredient(models.Model):
    """Ингредиент: продукт + количество в определённой единице измерения."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name='Продукт', null=True, on_delete=models.SET_NULL
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    measure = models.ForeignKey(
        Measure,
        verbose_name='Единица измерения',
        null=True,
        on_delete=models.SET_NULL,
    )
    group = models.ForeignKey(
        IngredientGroup,
        blank=True,
        null=True,
        default=1,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f'Рецепт {self.recipe.id}: {self.product}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
