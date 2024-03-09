from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.


def test_search(request):
    return HttpResponse("Hello, world. You're at the Test Search page")
