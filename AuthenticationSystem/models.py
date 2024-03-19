from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username


class UserVisit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.page} - {self.timestamp}"