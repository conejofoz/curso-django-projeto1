from django.http import Http404
from django.shortcuts import redirect, render
from .forms import RegisterForm


def register_view(request):
    # Recuperar dos dados do formulário que estão na sessão do navegador
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    
    # Gravar os dados do formulário na sessão do navegador
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    """ return render(request, 'authors/pages/register_view.html', {
        'form': form,
    }) """

    return redirect('authors:register')