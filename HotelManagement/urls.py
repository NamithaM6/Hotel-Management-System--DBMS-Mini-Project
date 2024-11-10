"""
URL configuration for HotelManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView

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
    path('book_room/<int:room_id>/', views.book_room, name='book_room'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('bookings/', views.book_room, name='book_room'),
    path('invoice/', views.invoice, name='invoice'), # Booking page URL
    path('bookings/', views.book_room, name='bookings'),
    path('register/', views.signup, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("login/", views.custom_login_view, name="login"),
    path("staff/homepage/", views.staff_homepage, name="staff_homepage"),
    path("customer/homepage/", views.customer_homepage, name="customer_homepage"),
]




