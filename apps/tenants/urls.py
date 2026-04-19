from django.urls import path
from apps.tenants import views

app_name = 'tenants'

urlpatterns = [
    path('', views.TenantSettingsView.as_view(), name='settings'),
    path('members/', views.MemberListView.as_view(), name='members'),
    path('members/invite/', views.InviteMemberView.as_view(), name='invite'),
    path('members/<int:pk>/remove/', views.RemoveMemberView.as_view(), name='remove_member'),
]
