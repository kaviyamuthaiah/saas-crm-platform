"""
accounts/models.py

Custom User model with tenant association and role-based access control.
Every user belongs to exactly one Tenant (row-based multi-tenancy).
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended user model.
    - tenant: FK to Tenant (set at registration)
    - role:   'admin' can manage tenant settings; 'user' is a regular member
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='members',
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def is_tenant_admin(self):
        """Convenience: is this user the admin of their tenant?"""
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
