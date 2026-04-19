"""
tenants/forms.py
"""
from django import forms
from apps.tenants.models import Tenant, TenantSettings


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('name', 'logo', 'domain', 'plan')


class TenantSettingsForm(forms.ModelForm):
    class Meta:
        model = TenantSettings
        fields = ('primary_color', 'timezone', 'date_format', 'allow_registration')
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
        }
