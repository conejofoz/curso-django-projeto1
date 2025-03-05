from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

from .tasks import my_send_email, send_email_simples, add, send_email_with_attachment


def register_view(request):
    # Recuperar dos dados do formulário que estão na sessão do navegador
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    
    # Gravar os dados do formulário na sessão do navegador
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Seu usuário foi criado, por favor faça login.') # falta implementar no html
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html',{
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()
    
    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user:
            messages.success(request, 'Você está logado')
            login(request, authenticated_user)
        else:    
            messages.error(request, 'Credenciais inválidas')
    else:    
        messages.error(request, 'Usuário ou senha inválidos')
    
    return redirect(login_url)
    #return render(request, 'authors/pages/login.html')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
    
    logout(request)
    return redirect(reverse('authors:login'))


def celery_view(request):
    # my_send_email.delay()
    # send_email_simples.delay()
    send_email_with_attachment.delay()
    # add.delay()
    return HttpResponse('Email enviado com sucesso!')