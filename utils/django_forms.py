import re
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