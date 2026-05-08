"""
crm/forms.py
"""
from django import forms
from apps.crm.models import Lead, Contact,Estimate


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

class EstimateForm(forms.ModelForm):

    class Meta:
        model = Estimate

        fields = (
            'lead',
            'estimate_number',
            'estimate_date',
            'expiry_date',
            'subtotal',
            'tax',
            'discount',
            'total_amount',
            'status',
            'notes',
            'created_by',
        )

        widgets = {

            'estimate_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'expiry_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'notes': forms.Textarea(
                attrs={'rows': 3}
            ),

        }

    def __init__(self, *args, tenant=None, **kwargs):

        super().__init__(*args, **kwargs)

        if tenant:

            self.fields['lead'].queryset = Lead.objects.filter(
                tenant=tenant,
                is_converted=False
            )

            self.fields['created_by'].queryset = tenant.members.filter(
                is_active=True
            )
