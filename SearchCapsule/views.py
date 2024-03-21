from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm
from django.db.models import Q
from TimeCapsuleManagement.models import Capsule, Subscription, UserProfile
from django.utils import timezone
from django.db.models.functions import Lower


def search(request):
    # Check if the request is to toggle a subscription
    if 'toggle_subscription' in request.GET:
        capsule_id = request.GET.get('capsule_id')
        if capsule_id:
            capsule = get_object_or_404(Capsule, pk=capsule_id)
            # Assuming you have a way to identify the current user's profile
            # For demonstration, let's fetch the first UserProfile as a placeholder
            user_profile = UserProfile.objects.first()

            # Toggle the subscription status
            subscription, created = Subscription.objects.get_or_create(
                user=user_profile,
                capsule=capsule,
            )
            if not created:
                subscription.delete()
            # Redirect to avoid the toggle action being repeated on refresh
            return redirect('SearchCapsule:capsule_search')

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

    # Filtering logic (unchanged from your original code)
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

    # Sorting logic (unchanged from your original code)
    sort = request.GET.get('sort')
    if sort == 'date':
        capsules = capsules.order_by('unsealing_date')
    elif sort == 'name':
        capsules = capsules.annotate(lower_name=Lower('name')).order_by('lower_name')

    context = {
        'form': form,
        'posts': capsules,
    }

    return render(request, 'search.html', context)
