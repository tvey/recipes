from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.views.generic import (
#     ListView,
#     DetailView,
#     CreateView,
#     UpdateView,
#     DeleteView,
# )
# from django.contrib.auth.models import User

# from .models import Recipe, Ingredient


# def home(request):
#     recipes = Recipe.objects.all()
#     context = {'recipes': recipes, 'title': 'Home'}
#     return render(request, 'recipes/home.html', context)


# class RecipeListView(ListView):
#     model = Recipe
#     template_name = 'recipes/home.html'
#     context_object_name = 'recipes'
#     ordering = ['-date_added']
#     paginate_by = 2


# class RecipeAuthorListView(ListView):
#     model = Recipe
#     template_name = 'recipes/recipe_authors.html'
#     context_object_name = 'recipes'
#     paginate_by = 2

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Recipe.objects.filter(author=user).order_by('-date_added')


# class RecipeDetailView(DetailView):
#     model = Recipe
#     context_object_name = 'recipe'


# class RecipeCreateView(LoginRequiredMixin, CreateView):
#     model = Recipe
#     # context_object_name = 'recipe'
#     success_url = '/'
#     fields = ['title', 'summary', 'main_image', 'prep_time']
#     # how to add ingredients???

#     def form_valid(self, form):  # overriding the method
#         form.instance.author = self.request.user  # set the author to current logged-in user
#         return super().form_valid(form)
#         # setting author before super method gets ran


# class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Recipe
#     fields = ['title', 'summary', 'main_image', 'prep_time']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         recipe = self.get_object()  # object we're trying to update
#         if self.request.user == recipe.author:
#             return True
#         return False


# class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Recipe
#     success_url = '/'
#     context_object_name = 'recipe'

#     def test_func(self):
#         recipe = self.get_object()
#         if self.request.user == recipe.author:
#             return True
#         return False
