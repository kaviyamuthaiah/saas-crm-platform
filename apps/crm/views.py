"""
crm/views.py

Tenant-aware CRUD views for Leads and Contacts.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.crm.models import Lead, Contact
from apps.crm.forms import LeadForm, ContactForm
from apps.tenants.mixins import TenantQuerysetMixin, TenantFormMixin


# ──────────────────────────────────────────────
# Contact Views
# ──────────────────────────────────────────────

class ContactListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    model = Contact
    template_name = 'crm/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(first_name__icontains=q) | qs.filter(
                last_name__icontains=q) | qs.filter(company__icontains=q)
        return qs


class ContactDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    model = Contact
    template_name = 'crm/contact_detail.html'
    context_object_name = 'contact'


class ContactCreateView(LoginRequiredMixin, TenantFormMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'crm/contact_form.html'
    success_url = reverse_lazy('crm:contact_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['tenant'] = self.request.tenant
        return kw

    def form_valid(self, form):
        messages.success(self.request, 'Contact created.')
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, TenantQuerysetMixin, TenantFormMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'crm/contact_form.html'
    success_url = reverse_lazy('crm:contact_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['tenant'] = self.request.tenant
        return kw

    def form_valid(self, form):
        messages.success(self.request, 'Contact updated.')
        return super().form_valid(form)


class ContactDeleteView(LoginRequiredMixin, TenantQuerysetMixin, DeleteView):
    model = Contact
    template_name = 'crm/contact_confirm_delete.html'
    success_url = reverse_lazy('crm:contact_list')

    def form_valid(self, form):
        messages.success(self.request, 'Contact deleted.')
        return super().form_valid(form)


# ──────────────────────────────────────────────
# Lead Views
# ──────────────────────────────────────────────

class LeadListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    model = Lead
    template_name = 'crm/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(company__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Lead.Status.choices
        return ctx


class LeadDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'


class LeadCreateView(LoginRequiredMixin, TenantFormMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'
    success_url = reverse_lazy('crm:lead_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['tenant'] = self.request.tenant
        return kw

    def form_valid(self, form):
        messages.success(self.request, 'Lead created.')
        return super().form_valid(form)


class LeadUpdateView(LoginRequiredMixin, TenantQuerysetMixin, TenantFormMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'
    success_url = reverse_lazy('crm:lead_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['tenant'] = self.request.tenant
        return kw

    def form_valid(self, form):
        messages.success(self.request, 'Lead updated.')
        return super().form_valid(form)


class LeadDeleteView(LoginRequiredMixin, TenantQuerysetMixin, DeleteView):
    model = Lead
    template_name = 'crm/lead_confirm_delete.html'
    success_url = reverse_lazy('crm:lead_list')

    def form_valid(self, form):
        messages.success(self.request, 'Lead deleted.')
        return super().form_valid(form)
