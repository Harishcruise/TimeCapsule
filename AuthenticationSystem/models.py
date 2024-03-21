import os

from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.


def user_profile_pic_path(instance, filename):
    # Generate filename based on user's id
    return os.path.join('static/images/', str(instance.id), filename)


class UserProfile(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profilepic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)

    def __str__(self):
        return self.username


class UserVisit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.page} - {self.timestamp}"
