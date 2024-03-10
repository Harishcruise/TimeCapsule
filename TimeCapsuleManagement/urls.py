from django.urls import path
from . import views

app_name = 'TimeCapsuleManagement'
urlpatterns = [
    path('', views.home, name='home'),
    path('mycapsules/', views.my_capsules, name='my_capsules')
]
