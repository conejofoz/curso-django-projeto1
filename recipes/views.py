from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    #return HttpResponse('HOME')
    return render(request, 'recipes/pages/home.html', context={'name': 'conejo'})


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={'name': 'conejo'})

# Create your views here.
