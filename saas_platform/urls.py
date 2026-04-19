"""
Root URL configuration for saas_platform.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('crm/', include('apps.crm.urls', namespace='crm')),
    path('settings/', include('apps.tenants.urls', namespace='tenants')),
    # Root redirect → dashboard
    path('', RedirectView.as_view(pattern_name='dashboard:index', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
