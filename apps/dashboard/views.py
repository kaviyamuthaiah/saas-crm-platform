"""
dashboard/views.py

Aggregates tenant-scoped statistics for the dashboard overview.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Sum, Q
from django.utils import timezone

from apps.projects.models import Project, Task
from apps.crm.models import Lead, Contact


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tenant = self.request.tenant
        today = timezone.now().date()

        # ── Project stats ──────────────────────────────
        ctx['total_projects'] = Project.objects.filter(tenant=tenant).count()
        ctx['active_projects'] = Project.objects.filter(tenant=tenant, status=Project.Status.ACTIVE).count()

        # ── Task stats ────────────────────────────────
        tasks_qs = Task.objects.filter(tenant=tenant)
        ctx['total_tasks'] = tasks_qs.count()
        ctx['tasks_done'] = tasks_qs.filter(status=Task.Status.DONE).count()
        ctx['tasks_overdue'] = tasks_qs.exclude(
            status=Task.Status.DONE
        ).filter(due_date__lt=today).count()
        ctx['my_tasks'] = tasks_qs.filter(
            assignee=self.request.user
        ).exclude(status=Task.Status.DONE)[:5]

        # ── CRM stats ─────────────────────────────────
        ctx['total_leads'] = Lead.objects.filter(tenant=tenant).count()
        ctx['open_leads'] = Lead.objects.filter(
            tenant=tenant
        ).exclude(status__in=[Lead.Status.WON, Lead.Status.LOST]).count()
        ctx['total_contacts'] = Contact.objects.filter(tenant=tenant).count()

        pipeline_value = Lead.objects.filter(
            tenant=tenant
        ).exclude(status__in=[Lead.Status.WON, Lead.Status.LOST]).aggregate(
            total=Sum('value')
        )['total'] or 0
        ctx['pipeline_value'] = pipeline_value

        # ── Recent activity ────────────────────────────
        ctx['recent_projects'] = Project.objects.filter(tenant=tenant).order_by('-created_at')[:5]
        ctx['recent_leads'] = Lead.objects.filter(tenant=tenant).order_by('-created_at')[:5]

        # ── Task status breakdown for chart ───────────
        task_breakdown = tasks_qs.values('status').annotate(count=Count('id'))
        ctx['task_chart_data'] = {
            item['status']: item['count'] for item in task_breakdown
        }

        return ctx
