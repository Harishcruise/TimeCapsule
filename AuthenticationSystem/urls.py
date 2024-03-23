from django.urls import path
from . import views
from .views import (
    PasswordResetView,
)

app_name = 'AuthenticationSystem'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_signup, name='user_signup'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.update_profile_picture, name='update_profile_picture'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
]
