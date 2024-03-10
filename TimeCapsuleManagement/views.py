from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Capsule, CapsuleContent, Comment, Subscription
from AuthenticationSystem.models import UserProfile
from .forms import CapsuleForm


# Create your views here.


def home(request):
    return render(request, 'home.html')


def my_capsules(request):
    if request.method == 'POST':
        form = CapsuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Time Capsule created successfully!')
            return redirect('TimeCapsuleManagement:my_capsules')
    else:
        form = CapsuleForm()
    return render(request, 'my_capsules.html', {'form': form})
