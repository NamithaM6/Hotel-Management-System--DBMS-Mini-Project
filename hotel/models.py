from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Define custom User model
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    )
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
