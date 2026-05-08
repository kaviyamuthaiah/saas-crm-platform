"""
crm/models.py

CRM module: Leads (potential customers) and Contacts (known people).
Both are scoped to a Tenant.
"""
from django.db import models
from apps.tenants.models import Tenant
from apps.accounts.models import User


class Contact(models.Model):
    """A known person in the CRM."""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['last_name', 'first_name']


class Lead(models.Model):
    """A sales lead / opportunity."""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        QUALIFIED = 'qualified', 'Qualified'
        PROPOSAL = 'proposal', 'Proposal Sent'
        WON = 'won', 'Won'
        LOST = 'lost', 'Lost'

    class Source(models.TextChoices):
        WEBSITE = 'website', 'Website'
        REFERRAL = 'referral', 'Referral'
        COLD_CALL = 'cold_call', 'Cold Call'
        SOCIAL = 'social', 'Social Media'
        EVENT = 'event', 'Event'
        OTHER = 'other', 'Other'

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leads')
    title = models.CharField(max_length=200, help_text='Brief description, e.g. "Website redesign for Acme"')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    company = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.OTHER)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='Estimated deal value')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    notes = models.TextField(blank=True)
    expected_close_date = models.DateField(null=True, blank=True)

    # NEW FIELDS
    is_converted = models.BooleanField(default=False)

    converted_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Estimate(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SENT = 'sent', 'Sent'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='estimates'
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='estimates'
    )

    estimate_number = models.CharField(
        max_length=50,
        unique=True
    )

    title = models.CharField(max_length=255)

    estimate_date = models.DateField()

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.estimate_number
    
class EstimateItem(models.Model):

    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        related_name='items'
    )

    service_name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

