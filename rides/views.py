from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RideRequestForm, DriverLoginForm, RiderSignupForm, DriverSignupForm
from .models import RideRequest, RideType, RideStatus, Driver, Assignment

def home(request):
    # Now looks for rides/templates/home.html
    return render(request, 'home.html')

@login_required
def dashboard(request):
    my_rides = RideRequest.objects.filter(rider=request.user).order_by('-created_at')
    open_shares = RideRequest.objects.filter(
        ride_type=RideType.SHARING,
        is_share_open=True,
        shared_by__isnull=True,
        status=RideStatus.REQUESTED
    ).exclude(rider=request.user)[:10]
    # Now looks for rides/templates/dashboard.html
    return render(request, 'dashboard.html', {
        'my_rides': my_rides,
        'open_shares': open_shares
    })

@login_required
def create_ride(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.rider = request.user
            ride.base_fare = 50.00  # mock base fare
            if ride.ride_type == RideType.SHARING:
                ride.is_share_open = True
            ride.save()
            messages.success(request, 'Ride requested.')
            return redirect('rides:ride_detail', ride_id=ride.id)
    else:
        form = RideRequestForm()
    # Now looks for rides/templates/create_ride.html
    return render(request, 'create_ride.html', {'form': form})

@login_required
def ride_detail(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, rider=request.user)
    # Now looks for rides/templates/ride_detail.html
    return render(request, 'ride_detail.html', {'ride': ride})

@login_required
def join_share(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id)
    if ride.can_accept_share():
        ride.shared_by = request.user
        ride.is_share_open = False
        ride.save()
        messages.success(request, 'You joined this shared ride. Fare will be split by 2.')
        return redirect('rides:ride_detail', ride_id=ride.id)
    messages.error(request, 'This shared ride is not available to join.')
    return redirect('rides:dashboard')

@login_required
def assign_driver(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, rider=request.user)
    if ride.status != RideStatus.REQUESTED:
        messages.info(request, 'Ride already processed.')
        return redirect('rides:ride_detail', ride_id=ride.id)
    driver = Driver.objects.filter(is_active=True).order_by('?').first()
    Assignment.objects.create(ride=ride, driver=driver)
    ride.status = RideStatus.MATCHED
    ride.save()
    messages.success(request, 'Driver assigned.')
    return redirect('rides:ride_detail', ride_id=ride.id)

def driver_login(request):
    if request.method == 'POST':
        form = DriverLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and hasattr(user, 'driver_profile'):
                login(request, user)
                messages.success(request, f'Welcome back, {user.driver_profile.name}!')
                return redirect('rides:driver_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a driver account.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = DriverLoginForm()
    return render(request, 'driver_login.html', {'form': form})

@login_required
def driver_dashboard(request):
    if not hasattr(request.user, 'driver_profile'):
        messages.error(request, 'Access denied. Driver account required.')
        return redirect('home')
    driver = request.user.driver_profile
    assigned_rides = Assignment.objects.filter(driver=driver).select_related('ride').order_by('-assigned_at')
    return render(request, 'driver_dashboard.html', {
        'driver': driver,
        'assigned_rides': assigned_rides
    })

def rider_signup(request):
    if request.method == 'POST':
        form = RiderSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('rides:dashboard')
    else:
        form = RiderSignupForm()
    return render(request, 'rider_signup.html', {'form': form})

def driver_signup(request):
    if request.method == 'POST':
        form = DriverSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Driver account created successfully!')
            return redirect('rides:driver_dashboard')
    else:
        form = DriverSignupForm()
    return render(request, 'driver_signup.html', {'form': form})
