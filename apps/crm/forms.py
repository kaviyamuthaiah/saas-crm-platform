"""
crm/forms.py
"""
from django import forms
from apps.crm.models import Lead, Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'company', 'title', 'notes', 'owner')
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, tenant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tenant:
            self.fields['owner'].queryset = tenant.members.filter(is_active=True)


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'title', 'contact', 'company', 'email', 'phone',
            'status', 'source', 'value', 'owner', 'notes', 'expected_close_date',
        )
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'expected_close_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, tenant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tenant:
            self.fields['owner'].queryset = tenant.members.filter(is_active=True)
            self.fields['contact'].queryset = Contact.objects.filter(tenant=tenant)
