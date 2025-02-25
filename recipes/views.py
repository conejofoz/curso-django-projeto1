from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from utils.recipes.factory import make_recipe
from utils.pagination import make_pagination_range
from recipes.models import Recipe



def home(request):
    #return HttpResponse('HOME')
    """ return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)],
        }) """
    
    messages.success(request, 'Mensagem de sucesso!')
    messages.error(request, 'Mensagem de erro!')
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, 6)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page)
    
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
    
    return render(request, 'recipes/pages/category.html', 
                    context={
                      'recipes': recipes, 
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

# Create your views here.
