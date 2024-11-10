from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Define custom User model
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

# Room model
ROOM_TYPES = [
    ('single', 'Single'),
    ('double', 'Double'),
    ('suite', 'Suite'),
]

class Room(models.Model):
    room_type = models.CharField(max_length=50)
    available_rooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # Default price is $100.00
    description = models.TextField(default="No description available.")  # Default description text

    def __str__(self):
        return f"{self.room_type} Room - {self.available_rooms} available"

# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPES,
        default='single'
    )
    check_in_date = models.DateField(default=datetime.date.today)
    check_out_date = models.DateField(default=datetime.date.today)
    bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Booking for {self.user.username} - {self.room_type}"

# Profile model (Optional: If you want additional user profile data)
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

# User creation form to handle custom user sign-up
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type',)
