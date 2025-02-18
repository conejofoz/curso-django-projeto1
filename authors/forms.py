from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    # Criar campos extras no formulário
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
                'placeholder': 'Digite seu usuário',
                'class': 'alguma-classe-css'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha'
            })
        }
