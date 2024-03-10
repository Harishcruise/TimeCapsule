from django.urls import path
from .views import CapsuleSearchView

urlpatterns = [
    path('search/', CapsuleSearchView.as_view(), name='capsule_search'),
    # Add other URL patterns as needed
]