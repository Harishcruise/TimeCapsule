from django.urls import path
from . import views

app_name = 'TimeCapsuleManagement'
urlpatterns = [
    path('/', views.home, name='home'),
]
