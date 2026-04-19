from django.urls import path
from django.views.generic import RedirectView
from apps.dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
]
