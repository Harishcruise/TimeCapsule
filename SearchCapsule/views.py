from django.db.models import Q
from .forms import SearchForm
from TimeCapsuleManagement.models import Capsule
from django.shortcuts import render


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        sort_by = request.GET.get('sort_by')

        if query:
            posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(owner__username__icontains=query)
            )
        if sort_by == 'date':
            posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(filters).order_by(
                '-creation_date')
        elif sort_by == 'username':
            posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(filters).order_by(
                'owner__username')
        else:
            posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').all()
    else:
        posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').all()

    return render(request, 'search.html', {'form': form, 'posts': posts})


