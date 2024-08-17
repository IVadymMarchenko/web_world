from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, choices=[("admin", "Admin"), ("user", "User")], default="user"
    )
    is_active = models.BooleanField(default=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Налаштування related_name для уникнення конфліктів
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # нове ім'я для реверсного доступу
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",  # нове ім'я для реверсного доступу
        blank=True,
    )

    def __str__(self):
        return self.username
