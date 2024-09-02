from django.urls import path
from recipes.views import home, recipe


urlpatterns = [
    path('', home, name="recipes-home"),
    path('recipes/<int:id>/', recipe, name="recipes-recipe")
]
