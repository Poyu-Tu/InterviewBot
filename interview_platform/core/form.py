from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        helpTexts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'password1': (
                'Your password can’t be too similar to your other personal information.<br>'
                'Your password must contain at least 8 characters.<br>'
                'Your password can’t be a commonly used password.<br>'
                'Your password can’t be entirely numeric.'
            ),
            'password2': 'Enter the same password as before, for verification.'
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)