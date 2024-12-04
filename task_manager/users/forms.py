from django.contrib.auth.forms import BaseUserCreationForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "username",
                  "password1",
                  "password2",]


class CustomUserChangeForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', "username",)
