from django.db.models import Q
from .forms import SearchForm
from TimeCapsuleManagement.models import Capsule
from django.shortcuts import render


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        unsealed_date = form.cleaned_data.get('unsealed_date', None)
        sealed_date = form.cleaned_data.get('sealed_date', None)
        is_public = form.cleaned_data.get('is_public', None)

        filters = Q()
        if query:
            filters &= (Q(name__icontains=query) |
                        Q(description__icontains=query) |
                        Q(owner__username__icontains=query))

        if unsealed_date:
            filters &= Q(unsealing_date=unsealed_date)

        if sealed_date:
            filters &= Q(sealed_date=sealed_date)

        if is_public is not None:
            filters &= Q(is_public=is_public)

        posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(filters)
    else:
        posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').all()

    return render(request, 'search.html', {'form': form, 'posts': posts})
