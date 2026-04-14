from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Foodle SaaS Owner'
        CAFE_OWNER = 'CAFE_OWNER', 'Tenant Admin'
        MANAGER = 'MANAGER', 'Shift Manager'
        CASHIER = 'CASHIER', 'Counter Person'
        CHEF = 'CHEF', 'Kitchen Staff'

    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.CAFE_OWNER,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
