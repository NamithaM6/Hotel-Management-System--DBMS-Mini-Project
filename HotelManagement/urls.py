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
    path('book_room/<str:room_type>/', views.book_room, name='book_room'),  # Use room_type instead of room_id
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('invoice/', views.invoice, name='invoice'),  # Booking page URL
    path('bookings/', views.bookings, name='bookings'),
    path('register/', views.signup, name='register'),
    path("login/", views.custom_login_view, name="login"),
    path("staff/homepage/", views.staff_homepage, name="staff_homepage"),
    path("customer/homepage/", views.customer_homepage, name="customer_homepage"),
    path('book_room/', views.book_room, name='book_room'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
