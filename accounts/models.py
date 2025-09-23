from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import random

class Profile(models.Model):
    USER_ROLES = [
        ('guest', 'Guest'),
        ('customer', 'Customer'),
        ('architect', 'Architect'),
        # ('admin', 'Admin'),  # use is_staff / is_superuser instead
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='guest')
    phone = models.CharField(max_length=20, blank=True, null=True)
    assigned_architect = models.CharField(max_length=100, blank=True, null=True)
    project_name = models.CharField(max_length=200, blank=True, null=True)
    project_start = models.DateField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"OTP for {self.user.username} - {self.code}"


# 🔔 Signals outside the model class - TEMPORARILY DISABLED
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         # Use get_or_create to prevent IntegrityError from race conditions
#         Profile.objects.get_or_create(
#             user=instance, 
#             defaults={'role': 'customer'}
#         )
#     else:
#         # Only save if profile exists
#         if hasattr(instance, 'profile'):
#             instance.profile.save()