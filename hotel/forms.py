# forms.py
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']

class CustomerSignUpForm(UserCreationForm):
    user_type_choices = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    
    user_type = forms.ChoiceField(choices=user_type_choices)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']
