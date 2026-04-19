"""
tenants/mixins.py

Reusable mixins for tenant-aware class-based views.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class TenantQuerysetMixin:
    """
    Automatically filters querysets to the current tenant.
    Use this in every ListView / DetailView / UpdateView / DeleteView
    to prevent data leakage between tenants.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(tenant=self.request.tenant)


class TenantFormMixin:
    """
    Automatically stamps the tenant FK on new objects before saving.
    Use in CreateView and UpdateView.
    """

    def form_valid(self, form):
        form.instance.tenant = self.request.tenant
        return super().form_valid(form)


class AdminRequiredMixin(LoginRequiredMixin):
    """
    Restricts a view to tenant admins only.
    Regular users get a 403.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_tenant_admin():
            raise PermissionDenied('Only workspace admins can access this page.')
        return super().dispatch(request, *args, **kwargs)
