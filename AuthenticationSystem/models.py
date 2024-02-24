from django.db import models
from django.contrib.auth.models import User


class TimeCapsules(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    unseal_date = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class CapsuleContent(models.Model):
    DOCUMENT_TYPES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('text', 'Text'),
    )

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_size = models.IntegerField()
    document = models.FileField(upload_to='capsule_content/')
    time_capsule = models.ForeignKey(TimeCapsules, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.document_type} - {self.time_capsule.title}"
