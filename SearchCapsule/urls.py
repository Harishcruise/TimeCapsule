from django.urls import path
from . import views

app_name = 'SearchCapsule'
urlpatterns = [
    path('search/', views.search, name='capsule_search'),
    # Add other URL patterns as needed
]
