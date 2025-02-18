# curso-django-projeto1


### Criar novo app
- python manage.py startapp authors
- adicionar o novo app no INSTALLED_APPS


### Criar a estrutura de pastas
- templates > authors > pages > register_view.html


### Criar uma view simples
```python
from django.shortcuts import render

def register_view(request):
    return render(request, 'authors/pages/register_view.html')
```


### Criar o urls.py do novo app

```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register_view')
]
```


### Adicionar as urls do novo app a url do projeto

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('authors/', include('authors.urls')) # <------
]
```


## Trabalhando com forms

- Criar o arquivo forms.py
- Criar a classe correspondente no forms.py
- Importar essa classe na view
- Na view criar uma instância da classe e passar no contexto retornado para a view


#### Importações
```python
from django.forms import Form, ModelForm
# ou
from django import forms
```


#### Criando um form simples
```python
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__' # ativando modo preguiça
        fields = ['first_name', 'last_name', 'username', 'email','password',]
```


#### Importando a classe RegisterForm na view e retornando no contexto
```python
from django.shortcuts import render
from .forms import RegisterForm


def register_view(request):
    form = RegisterForm()
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })
```



#### Exibindo o formulário no html

Só assim já apareceria os campos na tela mais não é assim que famos vazer:
```python
{{form}}
```
