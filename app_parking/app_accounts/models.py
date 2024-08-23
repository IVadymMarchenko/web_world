from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class User(AbstractUser):
    RATE_CHOICES = [
        ("basic", "Basic"),
        ("premium", "Premium"),
        ("standard", "Standard"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, choices=[("admin", "Admin"), ("user", "User")], default="user"
    )
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(null=True, blank=True)

    # Custom related_name settings to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
    )


    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.FileField(upload_to='photo_for_users', max_length=500,null=True)

    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    