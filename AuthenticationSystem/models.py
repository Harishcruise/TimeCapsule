from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(User):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
