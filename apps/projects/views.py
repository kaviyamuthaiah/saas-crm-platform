"""
projects/views.py

Tenant-aware CRUD views for Projects and Tasks.
All querysets are filtered by request.tenant to prevent cross-tenant data leakage.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.projects.models import Project, Task
from apps.projects.forms import ProjectForm, TaskForm
from apps.tenants.mixins import TenantQuerysetMixin, TenantFormMixin


# ──────────────────────────────────────────────
# Project Views
# ──────────────────────────────────────────────

class ProjectListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10


class ProjectDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tasks'] = self.object.tasks.all()
        return ctx


class ProjectCreateView(LoginRequiredMixin, TenantFormMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully.')
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, TenantQuerysetMixin, TenantFormMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully.')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, TenantQuerysetMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')

    def form_valid(self, form):
        messages.success(self.request, 'Project deleted.')
        return super().form_valid(form)


# ──────────────────────────────────────────────
# Task Views
# ──────────────────────────────────────────────

class TaskListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    model = Task
    template_name = 'projects/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        # Optional: filter by project
        project_id = self.request.GET.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['projects'] = Project.objects.filter(tenant=self.request.tenant)
        ctx['status_choices'] = Task.Status.choices
        return ctx


class TaskCreateView(LoginRequiredMixin, TenantFormMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'
    success_url = reverse_lazy('projects:task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, TenantQuerysetMixin, TenantFormMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'
    success_url = reverse_lazy('projects:task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Task updated.')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, TenantQuerysetMixin, DeleteView):
    model = Task
    template_name = 'projects/task_confirm_delete.html'
    success_url = reverse_lazy('projects:task_list')

    def form_valid(self, form):
        messages.success(self.request, 'Task deleted.')
        return super().form_valid(form)
