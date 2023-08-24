from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from account.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'avatar')
