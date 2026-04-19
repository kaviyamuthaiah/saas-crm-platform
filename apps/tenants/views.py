"""
tenants/views.py

Settings views – only tenant admins can access these.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, View
from django.shortcuts import redirect, render, get_object_or_404

from apps.tenants.mixins import AdminRequiredMixin
from apps.tenants.models import Tenant, TenantSettings
from apps.tenants.forms import TenantForm, TenantSettingsForm
from apps.accounts.forms import InviteUserForm
from apps.accounts.models import User


class TenantSettingsView(AdminRequiredMixin, View):
    """Combined view: tenant profile + settings on one page."""
    template_name = 'tenants/settings.html'

    def get(self, request):
        tenant = request.tenant
        # Get or create settings object
        settings_obj, _ = TenantSettings.objects.get_or_create(tenant=tenant)
        tenant_form = TenantForm(instance=tenant)
        settings_form = TenantSettingsForm(instance=settings_obj)
        return render(request, self.template_name, {
            'tenant_form': tenant_form,
            'settings_form': settings_form,
        })

    def post(self, request):
        tenant = request.tenant
        settings_obj, _ = TenantSettings.objects.get_or_create(tenant=tenant)
        tenant_form = TenantForm(request.POST, request.FILES, instance=tenant)
        settings_form = TenantSettingsForm(request.POST, instance=settings_obj)
        if tenant_form.is_valid() and settings_form.is_valid():
            tenant_form.save()
            settings_form.save()
            messages.success(request, 'Workspace settings saved.')
            return redirect('tenants:settings')
        return render(request, self.template_name, {
            'tenant_form': tenant_form,
            'settings_form': settings_form,
        })


class MemberListView(AdminRequiredMixin, ListView):
    """List all users in the current tenant."""
    model = User
    template_name = 'tenants/members.html'
    context_object_name = 'members'

    def get_queryset(self):
        return User.objects.filter(tenant=self.request.tenant)


class InviteMemberView(AdminRequiredMixin, View):
    """Tenant admin invites a new user to the workspace."""
    template_name = 'tenants/invite.html'

    def get(self, request):
        return render(request, self.template_name, {'form': InviteUserForm()})

    def post(self, request):
        form = InviteUserForm(request.POST)
        if form.is_valid():
            form.save(tenant=request.tenant)
            messages.success(request, 'Team member invited successfully.')
            return redirect('tenants:members')
        return render(request, self.template_name, {'form': form})


class RemoveMemberView(AdminRequiredMixin, View):
    """Remove a user from the tenant (soft: deactivate)."""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, tenant=request.tenant)
        if user == request.user:
            messages.error(request, 'You cannot remove yourself.')
        else:
            user.is_active = False
            user.save()
            messages.success(request, f'{user.username} has been deactivated.')
        return redirect('tenants:members')
