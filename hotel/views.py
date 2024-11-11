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

@login_required
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    booking_count = user_bookings.count()  # Count the user's bookings
    
    if booking_count > 0:
        messages.info(request, f"You have {booking_count} existing booking(s).")

    return render(request, 'bookings.html', {'bookings': user_bookings})

@login_required
def room_service(request):
    return render(request, 'room_service.html')

def order_food(request):
    return render(request, 'order_food.html')
def clean_room(request):
    return render(request, 'clean_room.html') 
def book_buggy(request):
    return render(request, 'book_buggy.html')

# Room Booking View
@login_required
def book_room(request):
    if request.method == 'POST':
        room_type = request.POST.get('room_type')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # Check if all required fields are filled
        if not room_type or not check_in_date or not check_out_date:
            messages.error(request, "All fields are required.")
            return redirect('bookings')

        try:
            room = get_object_or_404(Room, room_type=room_type)

            if room.available_rooms > 0:
                # Calculate the number of nights between check-in and check-out
                check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
                check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
                nights = (check_out - check_in).days
                room_price = room.price  # Store room price in a variable
                # Calculate total bill using room price and nights
                total_bill = room.price * nights

                # Create the booking with the total bill
                booking = Booking(
                    user=request.user,
                    room_type=room_type,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    bill=total_bill , # Storing the calculated bill
                    nights=nights,
                    room_price=room_price
                )
                booking.save()

                # Decrease the available rooms
                room.available_rooms -= 1
                room.save()

                messages.success(request, f"Your {room_type} room has been booked successfully!")
            else:
                messages.error(request, f"Sorry, no {room_type} rooms are available.")
        except Room.DoesNotExist:
            messages.error(request, "Invalid room type selected.")

        return redirect('bookings')  # Redirect back to bookings page after booking
    else:
        # If the request is not POST, show the booking form
        return render(request, 'bookings.html')
    
@login_required
def cancel_all_bookings(request):
    try:
        # Fetch all bookings for the logged-in user
        user_bookings = Booking.objects.filter(user=request.user)

        # Iterate over all bookings to cancel them
        for booking in user_bookings:
            # Get the associated room and increase the available rooms
            room = get_object_or_404(Room, room_type=booking.room_type)
            room.available_rooms += 1
            room.save()
            
            # Delete the booking
            booking.delete()

        messages.success(request, "All your bookings have been successfully canceled.")
    except Exception as e:
        messages.error(request, f"An error occurred while canceling your bookings: {e}")
    
    return redirect('bookings')  # Redirect to the bookings page after cancellation


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
