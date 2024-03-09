from django.db import models
from TimeCapsuleManagement.models import Capsule

class SearchableCapsule(models.Model):
    capsule = models.OneToOneField(Capsule, on_delete=models.CASCADE, primary_key=True)
    # Add any additional fields for search functionality

    def __str__(self):
        return f"Searchable {self.capsule.name}"