"""
tenants/context_processors.py

Injects the current tenant into every template context so templates
can display the workspace name, logo, etc. without manual passing.
"""


def tenant_context(request):
    return {
        'current_tenant': getattr(request, 'tenant', None),
    }
