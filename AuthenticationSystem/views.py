from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomSigninForm


def user_login(request):
    if request.method == 'POST':
        form = CustomSigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('TimeCapsuleManagement:home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomSigninForm()
    return render(request, 'user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('SearchCapsule:capsule_search')
