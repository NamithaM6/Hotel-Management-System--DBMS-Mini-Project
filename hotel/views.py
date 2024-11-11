from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Room, Booking, User, Order, FoodItem,UserManager,UserProfile
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from decimal import Decimal
from .forms import SignUpDetailsForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse

# Home view
def home(request):
    if request.user.is_authenticated:
        messages.success(request, 'You have successfully logged in!')
    return render(request, 'home.html')

# Rooms view - Displays all available room types
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    booking_count = user_bookings.count()
    
    if booking_count > 0:
        messages.info(request, f"You have {booking_count} existing booking(s).")

    return render(request, 'bookings.html', {'bookings': user_bookings})

@login_required
def room_service(request):
    return render(request, 'room_service.html')



def cart(request):
    # Retrieve the cart from the session
    cart = request.session.get('cart', [])

    if request.method == 'POST':
        # Calculate the total amount using Decimal
        total_amount = sum(Decimal(item['price']) * item['quantity'] for item in cart)

        # Generate a bill and show the order message
        context = {
            'cart': cart,
            'total_amount': total_amount,
            'message': "Your order will be delivered soon!"
        }

        # Clear the cart after the order is placed
        request.session['cart'] = []
        return render(request, 'order_summary.html', context)

    return render(request, 'cart.html', {'cart': cart})


def order_food(request):
    # Check if the request is POST and handle cart addition
    if request.method == 'POST':
        # Get the food item ID and quantity
        food_item_id = request.POST.get('food_item_id')
        quantity = int(request.POST.get('quantity', 1))  # Default quantity is 1

        # Get the food item from the database
        food_item = FoodItem.objects.get(id=food_item_id)

        # Initialize cart in session if not already present
        if 'cart' not in request.session:
            request.session['cart'] = []

        # Add the food item to the cart (as a dictionary with quantity)
        cart = request.session['cart']
        existing_item = next((item for item in cart if item['id'] == food_item.id), None)
        
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            cart.append({
                'id': food_item.id,
                'name': food_item.name,
                'price': str(food_item.price),
                'quantity': quantity,
                'image_url': food_item.image.url
            })

        # Save the updated cart to the session
        request.session['cart'] = cart

        return redirect('cart')  # Redirect to cart page

    # For GET request, just display the menu
    menu_items = FoodItem.objects.all()
    return render(request, 'order_food.html', {'menu_items': menu_items})

def update_cart(request, order_id):
    """Update the quantity of an item in the cart."""
    order = Order.objects.get(id=order_id, user=request.user, ordered=False)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        order.quantity = quantity
        order.save()
    return redirect('order_food')

@login_required
def order_summary(request):
    orders = Order.objects.filter(user=request.user)
    total_bill = sum(order.total_price for order in orders)
    return render(request, 'order_summary.html', {'orders': orders, 'total_bill': total_bill})

# Room Booking View

@login_required
def book_room(request):
    if request.method == 'POST':
        room_type = request.POST.get('room_type')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        if not room_type or not check_in_date or not check_out_date:
            messages.error(request, "All fields are required.")
            return redirect('bookings')

        try:
            room = get_object_or_404(Room, room_type=room_type)

            if room.available_rooms > 0:
                check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
                check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
                nights = (check_out - check_in).days
                room_price = room.price
                total_bill = room.price * nights

                booking = Booking(
                    user=request.user,
                    room_type=room_type,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    bill=total_bill,
                    nights=nights,
                    room_price=room_price
                )
                booking.save()

                room.available_rooms -= 1
                room.save()

                messages.success(request, f"Your {room_type} room has been booked successfully!")
            else:
                messages.error(request, f"Sorry, no {room_type} rooms are available.")
        except Room.DoesNotExist:
            messages.error(request, "Invalid room type selected.")

        return redirect('bookings')
    else:
        return render(request, 'bookings.html')

@login_required
def cancel_all_bookings(request):
    try:
        user_bookings = Booking.objects.filter(user=request.user)

        for booking in user_bookings:
            room = get_object_or_404(Room, room_type=booking.room_type)
            room.available_rooms += 1
            room.save()

            booking.delete()

        messages.success(request, "All your bookings have been successfully canceled.")
    except Exception as e:
        messages.error(request, f"An error occurred while canceling your bookings: {e}")

    return redirect('bookings')

@login_required
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)

        room = Room.objects.get(room_type=booking.room_type)
        room.available_rooms += 1
        room.save()

        booking.delete()

        messages.success(request, "Your booking has been successfully canceled.")
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")

    return redirect('home')

@login_required
def invoice(request):
    booking = Booking.objects.filter(user=request.user).last()
    return render(request, 'invoice.html', {'booking': booking})

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = SignUpDetailsForm(request.POST)
        if form.is_valid():
            return redirect('login')
    else:
        form = SignUpDetailsForm()
    return render(request, 'signup.html', {'form': form})

# Custom Login View
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # Get the user type (customer/staff)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Ensure user_type matches the one in the database
            if user.user_type == user_type:
                login(request, user)

                # Redirect based on user type
                if user.user_type == 'customer':
                    return redirect('home')  # Redirect to home.html for customers
                elif user.user_type == 'staff':
                    return redirect('staff_homepage')  # Redirect to staff_homepage.html for staff
            else:
                messages.error(request, "User type mismatch. Please select the correct user type.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def clean_room(request):
    return render(request, 'clean_room.html') 
def book_buggy(request):
    return render(request, 'book_buggy.html')

def update_cart(request, order_id):
    # Logic for updating the cart goes here
    # For example, you can fetch the order using the order_id and update its details.
    return HttpResponse(f"Cart for order ID {order_id} updated successfully.")

def staff_homepage(request):
    # Staff homepage logic here
    return render(request, "staff_homepage.html")