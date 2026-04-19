"""
tenants/models.py

The Tenant model is the core of our row-based multi-tenancy.
Every piece of data (projects, leads, contacts, tasks) has a FK to Tenant.
"""
from django.db import models


class Tenant(models.Model):
    """
    Represents a single organisation / workspace.
    All user data is scoped to a tenant via FK.
    """
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)
    domain = models.CharField(max_length=255, blank=True, help_text='Custom domain (optional)')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Plan / billing metadata (extendable)
    plan = models.CharField(
        max_length=20,
        choices=[('free', 'Free'), ('pro', 'Pro'), ('enterprise', 'Enterprise')],
        default='free',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TenantSettings(models.Model):
    """
    Key-value settings store per tenant.
    Extendable without schema changes.
    """
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='settings')
    primary_color = models.CharField(max_length=7, default='#4f46e5')
    timezone = models.CharField(max_length=50, default='UTC')
    date_format = models.CharField(max_length=20, default='%Y-%m-%d')
    allow_registration = models.BooleanField(default=False, help_text='Allow public sign-up under this tenant')

    def __str__(self):
        return f'Settings for {self.tenant}'
