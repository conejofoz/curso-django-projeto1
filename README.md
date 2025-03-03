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
---
## Messages - flash messages

- importação
```python
from django.contrib.messages import success, error, debug, warning, info
# ou direto
from django.contrib import messages
```

#### Enviando uma mensagem
- Para enviar uma mensagem tem que enviar o request e a mensagem
- Ela deve ser implementada em view do django.
- A variável messages é enviada no contexto automaticamente pelo Django.

```python
messages.success(request, 'Sua mensagem!')

```


#### Exibindo no template

- Deve ser feito um loop no template pois a variável messages é uma lista
```python
{% if messages %}
    <div class="main-content center container">
        {% for message in messages %}
            {{ message }}
        {% endfor %}
    </div>
{% endif %}
```

#### Configurando as tags, css de cada tipo de mensagem

settings.py
```python
from django.contrib.messages import constants


MESSAGE_TAGS = {
    constants.DEBUG: 'message-debug',
    constants.ERROR: 'message-error',
    constants.INFO: 'message-info',
    constants.SUCCESS: 'message-success',
    constants.WARNING: 'message-warning',
}
```
Agora as classes CSS devem ser criadas com esses nomes.

##### E como o Django sabe qual tag deve ser usada na mensagem no template html?
Na tag class da div onde vai ser exibida a mensagem colocar: {{ message.tags }}
Ficando assim:
```python
{% if messages %}
    <div class="main-content center container">
        {% for message in messages %}
            <div class="message {{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    </div>
{% endif %}
```


---
## Paginação com Django

from django.core.paginator import Paginator

Primeiro lugar ler a documentação, lá já tem um exemplo básico.

### Paginação com function based view

Criar uma instância da classe Paginator passando o queryset e a quantidade de páginas

Olhar o código no github, muito complicado


---
## Variaveis de ambiente no Django

pip install python-dotenv


Criar o arquivo .env e colocar as variáveis Ex: PER_PAGE=9
Criar o arquivo .env-exemple com dados fake, que é para os novos desenvolvedores pegarem como exemplo

Como usar:
from dotenv import load_dotenv
load_dotenv()

PER_PAGE = os.environ.get('PER_PAGE', 2)
PER_PAGE = os.getenv('PER_PAGE', 2)

Possíveis locais onde se deve importar o python-dotenv
manage.py
settings.py
asgy.py
wsgy.py

**Boas práticas:**
Não commit o arquivo .env: Adicione .env ao seu .gitignore para evitar que informações sensíveis sejam commitadas no repositório.

Use .env.example: Crie um arquivo .env.example com as chaves necessárias, mas sem os valores sensíveis, para que outros desenvolvedores saibam quais variáveis de ambiente precisam ser configuradas.

**Conclusão:**
O dotenv é uma ferramenta simples e eficaz para gerenciar variáveis de ambiente em projetos Django, especialmente em ambientes de desenvolvimento e produção. Ele ajuda a manter as configurações sensíveis seguras e fora do código-fonte, seguindo boas práticas de segurança.

---
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



#### Validação de campos
##### Validação campo a campo

Precisamos saber o nome do campo que queremos validar pois o Django concatena o nome do campo com
o nome do metodo clean. Isso no caso de validação campo a campo.

Temos duas maneiras de pegar os dados do campo:
- self.data, pega os dados crus.
- self.cleaned_data, pega os dados já tratados pelo Django.

Ex:

```Python
def clean_password(self):
    data = self.cleaned_data.get('password')

    if 'senha' in data:
        raise forms.ValidationError(
            'Não digite %(value)s no campo password',
            code='invalid',
            params={'value': '"senha"'}
        )
    
    return data
```

##### Validação vários campos

```python
def clean(self):
    cleaned_data = super().clean()

    password = cleaned_data.get('password')
    password2 = cleaned_data.get('password2')

    if password != password2:
        raise ValidationError({
            'password': 'As senhas devem ser iguais',
            # Também é possível usar um ValidationError dentro de outro
            'password2': ValidationError(
                'As senhas devem ser iguais',
                code='invalid'
            )
        })

```

Também é possível passar uma lista de validações:
```python
def clean(self):
    cleaned_data = super().clean()

    password = cleaned_data.get('password')
    password2 = cleaned_data.get('password2')

    if password != password2:
        password_confirmation_error = ValidationError(
                'As senhas devem ser iguais',
                code='invalid'
        )

        raise ValidationError({
            'password': password_confirmation_error,
            'password2': [
                password_confirmation_error,
                'outroerro'
            ] 
            
        })
```