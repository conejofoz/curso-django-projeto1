import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '') # concatena com o que já tem
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_var):
    #field.widget.attrs['placeholder'] = placeholder_var
    add_attr(field, 'placeholder', placeholder_var)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter no mínimo uma letra maiúscula, '
            'uma letra minúscula e um número. E nó mínimo 8 characteres.'
        ))

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')
        add_attr(self.fields['username'], 'class', 'fundo-azul')
        add_attr(self.fields['username'], 'class', 'letra-branca')


    # Criar campos extras no formulário ou sobrescrever os que já existem
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        }),
        error_messages={
            'required': 'A senha não pode ficar vazia'
        },
        validators=[strong_password]
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        })
    )
    # Sobrescrever campos que estão em fields, colocar aqui também. Já com tudo aqui também
    # como widget, help_texts...


    class Meta:
        model = User
        # fields = '__all__' # ativando modo preguiça
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'password',
        ]

        labels = {
            'username': 'Login'
        }

        help_texts = {
            'email': 'O e-mail é obrigatório',
        }

        error_messages = {
            # aqui as validações são por código, ex: required
            'username': {
                'required': 'Este campor é requerido'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                # 'placeholder': 'Digite seu usuário',
                'class': 'alguma-classe-css'
            }),
            'password': forms.PasswordInput(attrs={
                # 'placeholder': 'Digite sua senha'
            })
        }

    # Validação
    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'senha' in data:
            raise ValidationError(
                'Não digite %(value)s no campo password',
                code='invalid',
                params={'value': '"senha"'}
            )
        
        return data
    

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        existis = User.objects.filter(email=email).exists()

        if existis:
            raise ValidationError('Esse email já existe', code='invalid')
    
        return email
    

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
