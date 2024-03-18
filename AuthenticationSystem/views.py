from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomLoginForm, CustomSignupForm
from AuthenticationSystem.crud_operations.auth_operations import create_user


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('TimeCapsuleManagement:home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('AuthenticationSystem:user_login')
    else:
        form = CustomLoginForm()
    return render(request, 'user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('SearchCapsule:capsule_search')


def user_signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            create_user(username, password, first_name, last_name, email, bio)
            messages.success(request, 'User created successfully')
            return redirect('AuthenticationSystem:user_login')
    else:
        form = CustomSignupForm()
    return render(request, 'user_signup.html', {'form': form})
