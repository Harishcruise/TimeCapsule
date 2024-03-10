from django.db import models
# from django.contrib.auth.models import User
from AuthenticationSystem.models import UserProfile
from django.utils import timezone

# Create your models here.


class Capsule(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='capsules', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edited_date = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    unsealing_date = models.DateTimeField()

    def is_unsealed(self):
        return timezone.now() >= self.unsealing_date

    def __str__(self):
        return self.name


class CapsuleContent(models.Model):
    FILE_TYPES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('text', 'Text'),
    )
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    file = models.FileField(upload_to='capsule_content/%Y/%m/%d/')
    capsule = models.ForeignKey(Capsule, related_name='media', on_delete=models.CASCADE, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.file.name}"


class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, related_name='subscriptions', on_delete=models.CASCADE)
    capsule = models.ForeignKey(Capsule, related_name='subscribers', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)  # For private capsules, approval needed
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.capsule.name}"


class Comment(models.Model):
    capsule = models.ForeignKey(Capsule, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='comments_on_capsules', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.capsule.name}'
