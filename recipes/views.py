from django.shortcuts import render
from django.http import HttpResponse
from utils.recipes.factory import make_recipe
from recipes.models import Recipe


def home(request):
    #return HttpResponse('HOME')
    """ return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)],
        }) """
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'recipes/pages/home.html', context={'recipes': recipes})

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id)
    return render(request, 'recipes/pages/home.html', context={'recipes': recipes})

def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', 
                  context={
                    'recipe': make_recipe(),
                    'is_detail_page': True,
                  }
    )

# Create your views here.
