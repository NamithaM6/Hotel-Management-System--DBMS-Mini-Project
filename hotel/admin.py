from django.contrib import admin


from .models import Room,Booking,FoodItem,User

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(FoodItem)
admin.site.register(User)
# Register your models here.
