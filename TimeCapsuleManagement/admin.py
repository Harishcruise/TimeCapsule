from django.contrib import admin
from .models import Capsule, CapsuleMedia, Subscription, Comment

# Register your models here.
admin.site.register(Capsule)
admin.site.register(CapsuleMedia)
admin.site.register(Subscription)
admin.site.register(Comment)
