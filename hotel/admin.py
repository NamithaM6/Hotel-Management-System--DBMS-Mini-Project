from django.contrib import admin


from .models import Room,Booking,FoodItem

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(FoodItem)

# Register your models here.
