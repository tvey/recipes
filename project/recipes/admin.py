from django.contrib import admin

from .models import (
    Category,
    Dish,
    Cuisine,
    Diet,
    Recipe,
    RecipeStep,
    Product,
    Measure,
    Ingredient,
    IngredientGroup,
)

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Cuisine)
admin.site.register(Diet)
admin.site.register(Product)
admin.site.register(Measure)


class IngredientInlines(admin.TabularInline):
    model = Ingredient
    extra = 1
    fields = ['group__name']


class RecipeStepInlines(admin.TabularInline):
    model = RecipeStep
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'updated']
    # readonly_fields = ['slug']
    fieldsets = [
        (None, {'fields': ['author']}),
        (None, {'fields': [('title', 'slug'), 'summary']}),
        (None, {'fields': ['total_cooking_time']}),
        (None, {'fields': ['main_image']}),
    ]
    inlines = [IngredientInlines, RecipeStepInlines]
