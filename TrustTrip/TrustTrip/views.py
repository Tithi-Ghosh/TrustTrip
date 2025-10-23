from django.shortcuts import render
from booking_n_service.models import BookingUserSide

def home(request):
    if hasattr(request.user, 'user_profile'):
        profile = 'user_profile'
    else:
        profile = 'driver_profile'

    bookings = BookingUserSide.objects.all

    return render(request, 'home.html',{'profile':profile,'bookings':bookings})