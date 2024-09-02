from django.urls import path
from recipes.views import home, recipe, category

app_name = 'recipes'

urlpatterns = [
    path('', home, name="home"),
    # por enquanto fica a mesma view só para não quebrar
    path('recipes/category/<int:category_id>/', category, name="category"),
    path('recipes/<int:id>/', recipe, name="recipe")
]
