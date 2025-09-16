from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    USER_ROLES = [
        ('guest', 'Guest'),
        ('customer', 'Customer'),
        ('architect', 'Architect'),
        # ('admin', 'Admin'),  # use is_staff / is_superuser instead
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='guest')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# 🔔 Signals outside the model class
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()