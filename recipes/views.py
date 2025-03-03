from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from utils.recipes.factory import make_recipe
# from utils.pagination import make_pagination_range
from utils.pagination import make_pagination
from recipes.models import Recipe

import os
from dotenv import load_dotenv
load_dotenv()
# PER_PAGE = os.environ.get('PER_PAGE', 2)
PER_PAGE = os.getenv('PER_PAGE', 2)

def home(request):
    #return HttpResponse('HOME')
    """ return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)],
        }) """
    print('per page',PER_PAGE)
    messages.success(request, 'Mensagem de sucesso!')
    messages.error(request, 'Mensagem de erro!')
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE, 4)
    
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        }
    )

def category(request, category_id):
    """ recipes = Recipe.objects.filter(category__id=category_id, is_published=True)
    title = recipes.first().category.name

    if not recipes:
        raise Http404('No recipes found') """
    
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True))

    title = recipes[0].category.name # como o nome diz, retorna uma lista

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE, 4)
    
    return render(request, 'recipes/pages/category.html', 
                    context={
                      'recipes': page_obj, 
                      'pagination_range': pagination_range,
                      'title': f'{title}'
                    }
        )


def recipe(request, id):

    #recipe = Recipe.objects.filter(id=id, is_published=True).first()
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
                    #'recipe': make_recipe(),
                    'recipe': recipe,
                    'is_detail_page': True,
                  }
    )


def search(request):
    search_term = request.GET.get('search', '').strip()
    print(search_term)
    if not search_term:
        raise Http404('No search term provided')
    
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
    ).order_by('-id')

    print(recipes)

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE, 4)

    return render(request, 'recipes/pages/search.html',{
        'page_title': f'Search results for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'aditional_url_query': f'&search={search_term}',
    })
