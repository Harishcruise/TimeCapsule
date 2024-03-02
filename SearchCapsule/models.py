from django.db import models

# search_capsule/models.py
from TimeCapsuleManagement.models import Capsule


class SearchableCapsule(models.Model):
    capsule = models.OneToOneField(Capsule, on_delete=models.CASCADE, primary_key=True)
    # Add any additional fields for search functionality

    def __str__(self):
        return f"Searchable {self.capsule.name}"


class AdvancedSearchFilter(models.Model):
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    capsule_name = models.CharField(max_length=100, null=True, blank=True)
    # Add other filters as needed

    def __str__(self):
        return f"Advanced Search Filter {self.pk}"


