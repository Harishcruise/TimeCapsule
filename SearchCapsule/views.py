from django.shortcuts import render
from .forms import SearchForm
from django.db.models import Q
from TimeCapsuleManagement.models import Capsule

def search(request):
    # Initialize your form with request.GET to capture query parameters
    form = SearchForm(request.GET)
    # Check if the form is submitted with valid data
    if form.is_valid():
        query = form.cleaned_data.get('q', '')  # Get the search query from the form
        # If a query exists, filter the posts based on the query; otherwise, retrieve all posts
        if query:
            posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').all()
    else:
        # If form is not valid or no form is submitted, display all posts
        posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').all()

    return render(request, 'search.html', {'form': form, 'posts': posts})
