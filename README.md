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

## Celery


- Instalação
```bash
pip install celery redis
pip install django-celery-results
```

- Criar o arquivo celery.py ao lado do settings.py

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')

app = Celery('projeto')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

```


- Configuração no __init__.py do projeto

```python
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ('celery_app',)
```


- Dentro de cada app criar um arquivo tasks.py
- Registrar o celery results no installed apps
'django_celery_results',
- Fazer migrações



- Configurar no settins.py onde o celery vai guargar os resultados das execuções e demais configurações

```python
CELERY_RESULT_BACKEND = 'django-db'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```



**Instalação do redis no linux**
sudo apt-get install redis
sudo /etc/init.d/regis-server status

Não é o meu caso, eu usei no docker.


- **rodar no linux**
celery -A projeto worker --loglevel=info
ou
celery -A projeto worker -l info


- **rodar no windows**
celery -A projeto worker --pool=solo --loglevel=info

- **fazer um teste**
python manage.py shell
from projeto.celery import debug_task
debug_task.delay() # já é para criar uma tarefa



## Agendamento de tarefas com Celery Beat

São baseadas por padrão no timezone de Londres, mas é possível modificar.

- Instalar o celery beat
- Adicionar no INSTALLED_APS
- Migrar as tabelas
- Configurar as tarefas no próprio django admin, ou manualmente via arquivos python.


```bash
pip install django-celery-beat
```


Adicionar no INSTALLED_APPS
'django_celery_beat',


**Rodar o celery beat**

Obs: No windows tem que rodar em um terminal diferente do que já está rodando o celery.
Já no linux pode rodar o mesmo comando que roda o celery com a opção -B


- Linux:

celery -A projeto worker --loglevel=info -B

- Windows:

celery -A projeto beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler


### Configuração para o vps

cd /etc/systemd/system/

nano celery.service


```bash
[Unit]
Description=Celery Service
after=network.target

[Service]
Type=forking
User=conejofoz
Group=conejofoz
WorkingDirectory=/home/conejofoz/projeto
ExecStart=/bin/sh -c '/home/conejofoz/venv/bin/celery -A projeto worker -l info -B --scheduler django_celery_beat.chedulers:DatabaseScheduler &'
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
´´´


# Laravel





--------------------------
docker


**wsl

wsl --install
wsl --status


/mnt/ é o computador

/mnt/c é a unidade c do windows


se entrar na pasta pelo windows e digitar wsl já muda pelo linux dentro da pasta



**docker instalação
entrar no site e fazer download


Caso já tenha a versão wsl 1 instalada tem que converter para 2

wsl --list --verbose

NAME      STATE           VERSION
* Ubuntu    Stopped         1
Aqui, a distribuição "Ubuntu" está na versão 1.

wsl --set-version Ubuntu 2
wsl --set-version Ubuntu 2conejo24


------------------------------
winget

procurar programas para instalar
winget search "docker" 


site para pesquisar os pacotes
winget.run

instalar vscode pelo winget, tem que usar o id
winget --install -e --id Microsoft.VisualStudioCode




--------------
laravel sail

Tem que ter o wsl2 e o docker instalados


Procurar o comando curl no site do laravel

e colar no terminal do wsl

curl -s https://laravel.build/example-app | bash

vai baixar o redis mysql e o scambal a 4


Subir os containers
Entrar na pasta do projeto
./vendor/bin/sail up -d

Parar os containers
./vendor/bin/sail stop

Todos os comandos do artisan tem que colocar esse vendor antes
./vendor/bin/sail artisan migrate



Escolhendo só os pacotes que eu quero, por exemplo só o mysql
curl -s "https://laravel.build/example-app?with=mysql, redis" | bash




***
Criando um apelido para o vendor 
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'

Agora é só digitar:
sail artisan migrate


Se abrir outro terminal já não funciona mais
Resolvendo:

se não soube qual bash é, digite nano ~/. que ele vai listar
nano ~/.

colar no inicio do arquivo:
nano ~/.bashrc
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'


se não soube qual bash é, digite nano ~/. que ele vai listar
nano ~/.


***
Erros:
dizia que sail não está rodando
solução: tem que levantar ele antes:
./vendor/bin/sail up
ou se ja tiver feita a configuração no bash somente:
sail up -d









----------------------------------------------------------------------------------------------
php artisan dicas
php artisan list







----------------------------------------------------------------------------------------
### Rotas


Route::get('admin/usuarios', [UserController::class, 'index']);

**Rota com parâmetro**
Route::get('admin/usuarios/{id}', [UserController::class,'show']);






---
### Blade

#### Herança de templates no blade

No pai:
@yeld('content')


Ex:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'Titulo padrão')</title>
</head>
<body>
    @yield('content')
</body>
</html>
```


No filho:
@extends
@section


Ex:

@extends('layouts.app')
@section('title', 'Listagem de usuários')
@section('content')

    @foreach ($users as $user)
        <div>{{$user->name}}</div>
    @endforeach

@endsection







--------------------------------------------------------------------------------------------------------------------------------
### Assets - js e css no laravel

npm i
npm run build

npm run dev - Não precisa ficar rodando o build a cada alteração

Atenção: verificar no package.json se o nome dos comandos não estão diferentes na sessão scripts.

O build vai ser feito dentro da pasta public/build/assets
Ou seja vai copiar os arquivos de resources/css e resources/js e resources/images para a pasta public



Imagens staticas:

Procuar na documentação do laravel por: 
- Asset Bundling (Vite)
-- Processing Static Assets With Vite


colar no app.js

import.meta.glob([
  '../images/**',
  '../fonts/**',
]);

Copiar suas imangens para dentro dessa pasta images, se não tiver crie, e quando fizer o build novamente elas serão copiadas 
para dentro da pasta public



#### Mostrar uma imagem no html

<img width="100" src="{{ Vite::asset('resources/images/jbl.jpg') }}" alt="Caixa de som JBL">




### Eloquent básico

Criar uma migration

php artisan make:migration create_posts_table

ou

sail artisan make:migration create_posts_table

Criar a migration através do model

php artisan make:model Post --migration


Rodar a migration

php artisan migrate


Desfazer a migration

php artisan migrate:rollback





#### Models

##### Configurar salvamento em massa

class Post extends Model
{
    protected $fillable = [
        'title', 'body'
    ];
}


##### Nome da tabela de sistema já existente

protected $table = 'post_erp';


##### Salvando um registro

$post = new Post();
$post->title = 'Meu primeiro post';
$post->body = 'Essa é a mensagem do corpo do post';
$post->save();


ou usando o método create, só que ele já cria na hora, não precisa do save()
$post = Post::create([
        'title'=> 'Meu segundo post',
        'body'=> 'Corpo do segundo post'

    ]);

    dd($post);

Obs: nos dois casos observei que ele já retorna o registro criado quando faço o dd()



##### Buscando os registros

Pra buscar um registro usar o find passando o id ou usar o where() com first()
$post = Post::find(2);
$post = Post::where('id',1)->first();


Pra buscar uma coleção, usar all() ou where com get()
$posts = Post::all();
$post = Post::where('title', 'LIKE', '%post%')->get();



### Atualizando registros

```php
/* Atualizar */
$post = Post::find(1);
$post->titulo = 'Meu novo titulo';
$post->save();
```

**Outra maneira de atualizar usando o método fill**

Uma outra maneira de atualizar passando um array com todos os campos para atualizar para o método fill()
```php
$input = [
    'title'=> 'Meu outro novo título',
    'body'=> 'Corpo do meu outro título'
];

$post = Post::find(1);
$post->fill($input);
$post->save();
```







	