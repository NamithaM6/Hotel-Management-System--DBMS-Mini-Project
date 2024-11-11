# forms.py
from django import forms
from .models import User,SignUpDetails
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


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

class SignUpDetailsForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    user_type = forms.ChoiceField(choices=[('customer', 'Customer'), ('staff', 'Staff'), ('admin', 'Admin')], required=True)

    # Optional: You can add validations here if needed
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    