from django.urls import path

from .views import index

app_name = 'recipes'

urlpatterns = [
   path('', index, name='home'), 
]


# from .views import (
#     RecipeListView,
#     RecipeDetailView,
#     RecipeCreateView,
#     RecipeUpdateView,
#     RecipeDeleteView,
#     RecipeAuthorListView,
# )
# from .views import home, about

# urlpatterns = [
#     # path('', home, name='recipes-home'),
#     path('', RecipeListView.as_view(), name='recipes-home'),
#     path('author/<int:pk>/', RecipeAuthorListView.as_view(), name='recipes-author'),
#     path('author/<int:pk>/<str:username>/', RecipeAuthorListView.as_view(), name='recipes-author'),
#     path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
#     path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
#     path('recipe/<int:pk>/<slug:slug>/', RecipeDetailView.as_view(), name='recipe-detail'),  # or redirect?
#     path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
#     path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
# ]
