from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Room, Booking, User
from .forms import CustomUserCreationForm  # Correct form for custom sign-up
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
def book_room(request):
    if request.method == 'POST':
        # Extract form data
        room_type = request.POST.get('room_type')
        check_in = request.POST.get('check_in_date')
        check_out = request.POST.get('check_out_date')
        
        try:
            # Convert the string dates to date objects
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

            # Calculate the number of days between the check-in and check-out dates
            num_days = (check_out_date - check_in_date).days
            
            # Fetch room by type
            room = Room.objects.get(room_type=room_type)
            
            if room.available_rooms > 0:
                # Decrease room availability by 1
                room.available_rooms -= 1
                room.save()

                # Calculate the bill based on the room price and the number of days
                bill = num_days * room.price  # Multiply price by number of days
                
                # Create a new booking record
                Booking.objects.create(
                    user=request.user,
                    room_type=room.room_type,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    bill=bill
                )

                # Success message
                messages.success(request, "Booking successful!")
                return redirect('bookings')
            else:
                messages.error(request, "No rooms available for the selected type.")
        except Room.DoesNotExist:
            messages.error(request, "Invalid room type selected.")
        except ValueError:
            messages.error(request, "Invalid date format.")
    return render(request, 'bookings.html')


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
                return redirect(reverse("staff_homepage"))  # Define this URL pattern in urls.py
            else:
                return redirect(reverse("customer_homepage"))  # Define this URL pattern for customer

        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

def staff_homepage(request):
    # Staff homepage logic here
    return render(request, "staff_homepage.html")

def customer_homepage(request):
    # Customer homepage logic here
    return render(request, "customer_homepage.html")
