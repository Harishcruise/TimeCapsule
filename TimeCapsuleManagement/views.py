from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Capsule, CapsuleContent, Comment, Subscription


# Create your views here.

def home(request):
    return render(request, 'home.html')


def my_capsules(request):
    return render(request, 'mycapsules.html')