from django.contrib import admin
from django.urls import path, include
from .views import advanced_search_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('advanced-search/', advanced_search_view, name='advanced_search_view'),
]
