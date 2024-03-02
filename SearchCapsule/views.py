from django.shortcuts import render

# Create your views here.

# search_capsule/views.py
from django.shortcuts import render

from .models import SearchableCapsule
from .models import AdvancedSearchFilter, Capsule


def capsule_search(request):
    query = request.GET.get('q', '')
    searchable_capsules = SearchableCapsule.objects.filter(capsule__name__icontains=query, capsule__is_public=True)

    context = {
        'query': query,
        'capsules': [searchable_capsule.capsule for searchable_capsule in searchable_capsules],
    }

    return render(request, 'search_capsule/capsule_search_results.html', context)


def advanced_search_view(request):
    if request.method == 'POST':
        # Process form submission and create/update the filter
        # Retrieve data based on the filter
        # Pass data to the template
        pass
    else:
        # Render advance search form
        filters = AdvancedSearchFilter.objects.all()
        return render(request, 'search_capsule/advanced_search.html', {'filters': filters})


