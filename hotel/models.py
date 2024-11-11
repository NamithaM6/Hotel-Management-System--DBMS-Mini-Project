from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
import datetime
from decimal import Decimal
from django.conf import settings

# Define custom User model
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username
    
# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

# Custom User model
class User(AbstractBaseUser, PermissionsMixin):  # Inherit from PermissionsMixin
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=(('customer', 'Customer'), ('staff', 'Staff')))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

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
    
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the food item
    ordered = models.BooleanField(default=False)  # tracks if the order is confirmed

    @property
    def total_price(self):
        return self.food_item.price * self.quantity

# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='single')
    check_in_date = models.DateField(default=datetime.date.today)
    check_out_date = models.DateField(default=datetime.date.today)
    bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    room_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nights = models.IntegerField(null=True)

    def __str__(self):
        return f"Booking for {self.user.username} - {self.room_type}"

class SignUpDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.user.username