from django.urls import path
from . import views

app_name = 'TimeCapsuleManagement'
urlpatterns = [
    path('', views.home, name='home'),
    path('my-capsules/', views.my_capsules, name='my_capsules'),
    path('delete_capsule/<int:capsule_id>/', views.delete_capsule, name='delete_capsule'),
    path('post_comment/<int:capsule_id>/', views.post_comment, name='post_comment')
]
