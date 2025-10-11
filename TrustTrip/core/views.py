from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import UserProfile


def reg_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # check if username exists
        if User.objects.filter(username=username).exists():
            return redirect('user:register_user')

        # create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = False  # Cannot access admin
        user.is_superuser = False  # Definitely not admin
        user.save()
        userProfile = UserProfile.objects.create(user=user)
        userProfile.save()
        login(request, user)
        return redirect('home')

    return render(request, 'core/reg_user.html')
