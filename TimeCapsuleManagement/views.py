from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Capsule, CapsuleContent, Comment, Subscription


# Create your views here.

def home(request):
    return render(request, 'home.html')

def test_capsules(request):
    return HttpResponse("Hello, world. You're at the Test Capsule page")
