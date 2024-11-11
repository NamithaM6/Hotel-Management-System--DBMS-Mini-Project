from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from hotel import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('rooms/', views.rooms, name='rooms'),
    path('book_room/', views.book_room, name='book_room'), # Use room_type instead of room_id
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('invoice/', views.invoice, name='invoice'),  # Booking page URL
    path('bookings/', views.bookings, name='bookings'),
    path('register/', views.signup_view, name='register'),
    path("login/", views.custom_login_view, name="login"),
    path("customer/homepage/", views.home, name="customer_homepage"),
    path('book_room/', views.book_room, name='book_room'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('cancel_all_bookings/', views.cancel_all_bookings, name='cancel_all_bookings'),
    path('room_service/', views.room_service, name='room_service'),
    path('order_food/', views.order_food, name='order_food'),
    path('clean_room/', views.clean_room, name='clean_room'),
    path('book_buggy/', views.book_buggy, name='book_buggy'), 
    path('order_food/', views.order_food, name='order_food'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/<int:order_id>/', views.update_cart, name='update_cart'),
    path('staff_homepage/', views.staff_homepage, name='staff_homepage'),
]
