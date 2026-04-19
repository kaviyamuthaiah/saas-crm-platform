from django.contrib import admin
from apps.tenants.models import Tenant, TenantSettings


class TenantSettingsInline(admin.StackedInline):
    model = TenantSettings
    can_delete = False


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'plan', 'is_active', 'created_at')
    list_filter = ('plan', 'is_active')
    inlines = [TenantSettingsInline]
