from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone


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
    license_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
