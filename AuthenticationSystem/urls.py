from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'AuthenticationSystem'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
]