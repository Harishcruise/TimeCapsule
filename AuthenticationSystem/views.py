from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import UserProfile

# Create your views here.


def login(request):
    return HttpResponse("Hello, world. You're at the Test Login page")
