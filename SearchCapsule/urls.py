from django.urls import path
from . import views

app_name = 'SearchCapsule'
urlpatterns = [
    path('search/', views.search, name='capsule_search'),
    path('toggle_subscription/<int:capsule_id>/', views.toggle_subscription, name='toggle_subscription'),

]
