from django.shortcuts import render

# Create your views here.

# search_capsule/views.py
from django.shortcuts import render

from .models import SearchableCapsule

def capsule_search(request):
    query = request.GET.get('q', '')
    searchable_capsules = SearchableCapsule.objects.filter(capsule__name__icontains=query, capsule__is_public=True)

    context = {
        'query': query,
        'capsules': [searchable_capsule.capsule for searchable_capsule in searchable_capsules],
    }

    return render(request, 'search_capsule/capsule_search_results.html', context)

