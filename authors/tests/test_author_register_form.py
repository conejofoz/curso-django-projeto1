from django.urls import reverse
from authors.forms import RegisterForm
from django.test import TestCase
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Digite seu nome'),
        ('last_name', 'Digite seu sobrenome'),
    ])

    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    """ def teste_email_field_must_be_unique(self):
        url = reverse('authors:create')
        
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Esse email já existe'
        self.assertIn(msg, response.content['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8')) """
    

    def test_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456'
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated =  self.client.login({
            'username': 'testuser',
            'password': '@Bc123456',
        })

        self.assertTrue(is_authenticated)
