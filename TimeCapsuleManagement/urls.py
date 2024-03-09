from django.urls import path
from . import views

app_name = 'TimeCapsuleManagement'
urlpatterns = [
    path('capsule/', views.test_capsules, name='test_capsules'),
]
