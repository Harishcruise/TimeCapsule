from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'AuthenticationSystem'
urlpatterns = [
    path('signin/', views.signin, name='signin'),
]