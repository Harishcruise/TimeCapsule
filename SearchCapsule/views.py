from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import SearchForm
from django.db.models import Q
from TimeCapsuleManagement.models import Capsule, Subscription, UserProfile
from django.utils import timezone
from django.db.models.functions import Lower
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
def search(request):
    # Handle the toggle subscription action
    if 'toggle_subscription' in request.GET:
        capsule_id = request.GET.get('capsule_id')
        if capsule_id:
            capsule = get_object_or_404(Capsule, pk=capsule_id)
            # Replace the following line with your method of getting the current user's profile
            user_profile = request.user.userprofile

            subscription, created = Subscription.objects.get_or_create(
                user=user_profile,
                capsule=capsule,
            )
            if not created:
                subscription.delete()  # If the subscription already exists, delete it (unsubscribe)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    form = SearchForm(request.GET)
    capsules = Capsule.objects.prefetch_related('media', 'comments', 'subscribers')

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

    # Check subscription status for each capsule for the current user (if logged in)
    if request.user.is_authenticated:
        user_profile = request.user.username
        for capsule in capsules:
            capsule.is_subscribed = capsule.subscribers.filter(user=user_profile).exists()
    else:
        for capsule in capsules:
            capsule.is_subscribed = False

    context = {
        'form': form,
        'posts': capsules,
    }

    return render(request, 'search.html', context)




def toggle_subscription(request, capsule_id):
    # Fetch the capsule object based on the provided capsule_id
    capsule = get_object_or_404(Capsule, pk=capsule_id)
    user_profile = request.user.username  # Assuming you have a userprofile attribute

    # Check if a subscription already exists for this user and capsule
    subscription, created = Subscription.objects.get_or_create(
        user=user_profile,
        capsule=capsule,
    )

    if not created:
        # If the subscription exists, delete it (unsubscribe)
        subscription.delete()
    # Redirect to the previous page or a specific page after toggling the subscription
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


