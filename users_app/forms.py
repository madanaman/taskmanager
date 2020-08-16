from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField()
    FirstName = forms.CharField(label="First Name", required=False)
    LastName = forms.CharField(label="Last Name", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'FirstName', 'LastName']
