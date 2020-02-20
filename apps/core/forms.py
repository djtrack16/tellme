from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from bootstrap.forms import BootstrapMixin, Fieldset
from django import forms

class BootstrapUserCreationForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        layout = (
            Fieldset(
                "Create an account", 
                "username", 
                "email",
                "password1", 
                "password2"),
            )


class BootstrapAuthenticationForm(BootstrapMixin, AuthenticationForm):
    class Meta:
        layout = (
            Fieldset(
                "Login", 
                "username", 
                "password"),
            )
