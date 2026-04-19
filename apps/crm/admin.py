from django.contrib import admin
from apps.crm.models import Lead, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'company', 'tenant', 'owner')
    list_filter = ('tenant',)
    search_fields = ('first_name', 'last_name', 'email', 'company')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'value', 'tenant', 'owner', 'created_at')
    list_filter = ('status', 'source', 'tenant')
    search_fields = ('title', 'company', 'email')
