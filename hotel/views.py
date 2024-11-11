from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Room, Booking, User
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse

# Home view
def home(request):
    if request.user.is_authenticated:
        messages.success(request, 'You have successfully logged in!')
    return render(request, 'home.html')

# Rooms view - Displays all available room types
def rooms(request):
    rooms = Room.objects.all()  # Fetch all rooms from the database
    return render(request, 'rooms.html', {'rooms': rooms})  # Pass rooms to the template

# Bookings view - Displays user bookings (only for authenticated users)
@login_required
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': user_bookings})

# Room Booking View
@login_required
def book_room(request, room_type):
    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # Check if the room type is available
        try:
            room = Room.objects.get(room_type=room_type)
            if room.available_rooms <= 0:
                messages.error(request, "Sorry, no rooms available for this type.")
                return redirect('book_room', room_type=room_type)

            # Create booking
            booking = Booking(
                user=request.user,
                room_type=room_type,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                bill=room.price,  # This can be modified to include the actual bill logic
            )
            booking.save()

            # Update room availability
            room.available_rooms -= 1
            room.save()

            messages.success(request, f"Booking successful! Your room type is {room_type}.")
            return redirect('invoice')  # Redirect to invoice page

        except Room.DoesNotExist:
            messages.error(request, "Invalid room type selected.")
            return redirect('book_room', room_type=room_type)

    return render(request, 'bookings.html', {'room_type': room_type})

@login_required
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)

        # Update room availability
        room = Room.objects.get(room_type=booking.room_type)
        room.available_rooms += 1
        room.save()

        # Delete the booking
        booking.delete()

        messages.success(request, "Your booking has been successfully canceled.")
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
    
    return redirect('home')  # Redirect to homepage after cancellation

# Invoice view to show booking details
@login_required
def invoice(request):
    booking = Booking.objects.filter(user=request.user).last()  # Latest booking for the user
    return render(request, 'invoice.html', {'booking': booking})

# Sign Up View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signing up
            messages.success(request, 'Your account has been created successfully! You are now logged in.')
            return redirect('home')  # Redirect to the home page after successful sign-up
        else:
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def custom_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.user_type == "staff":
                return redirect(reverse("staff_homepage"))
            else:
                return redirect(reverse("customer_homepage"))

        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

def staff_homepage(request):
    # Staff homepage logic here
    return render(request, "staff_homepage.html")

def customer_homepage(request):
    # Customer homepage logic here
    return render(request, "home.html")  # Use home.html for the customer homepage
