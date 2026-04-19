"""
tenants/middleware.py

TenantMiddleware attaches the current tenant to every request.
It reads the tenant from request.user (set at login time).
All views/queries then use request.tenant to filter data.
"""
from django.shortcuts import redirect
from django.contrib import messages


class TenantMiddleware:
    """
    Middleware that resolves the active tenant for each request.

    Strategy (row-based):
      1. If the user is authenticated, read user.tenant
      2. Attach it as request.tenant
      3. If the user has no tenant assigned, log them out gracefully
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default to None; unauthenticated pages work fine with no tenant
        request.tenant = None

        if request.user.is_authenticated:
            tenant = getattr(request.user, 'tenant', None)
            if tenant is None:
                # Edge case: authenticated user with no tenant (data issue)
                from django.contrib.auth import logout
                logout(request)
                messages.error(request, 'Your account is not linked to any workspace. Please contact support.')
                return redirect('accounts:login')

            if not tenant.is_active:
                from django.contrib.auth import logout
                logout(request)
                messages.error(request, 'Your workspace has been suspended. Please contact support.')
                return redirect('accounts:login')

            request.tenant = tenant

        response = self.get_response(request)
        return response
