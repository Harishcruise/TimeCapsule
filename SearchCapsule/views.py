from django.shortcuts import render
from .forms import SearchForm
from django.db.models import Q
from TimeCapsuleManagement.models import Capsule
from django.utils import timezone
from django.db.models.functions import Lower
def search(request):
    form = SearchForm(request.GET)
    capsules = Capsule.objects.prefetch_related('media').prefetch_related('comments')

    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        if query:
            capsules = capsules.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(owner__username__icontains=query)
            )

    # Filtering logic
    status = request.GET.get('status')
    sealed = request.GET.get('sealed')
    date = request.GET.get('date')

    if status == 'public':
        capsules = capsules.filter(is_public=True)
    elif status == 'private':
        capsules = capsules.filter(is_public=False)

    if sealed == 'unsealed':
        capsules = capsules.filter(unsealing_date__lte=timezone.now())
    elif sealed == 'sealed':
        capsules = capsules.filter(unsealing_date__gt=timezone.now())

    if date:
        capsules = capsules.filter(unsealing_date__date=date)

    # Sorting logic
    sort = request.GET.get('sort')
    if sort == 'date':
        capsules = capsules.order_by('unsealing_date')
    elif sort == 'name':
        capsules = capsules.annotate(lower_name=Lower('name')).order_by('lower_name')
        for capsule in capsules:
            print(capsule)

    context = {
        'form': form,
        'posts': capsules,
    }

    return render(request, 'search.html', context)