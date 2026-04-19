from django.contrib import admin
from apps.projects.models import Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('title', 'status', 'priority', 'assignee', 'due_date')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'status', 'owner', 'due_date')
    list_filter = ('status', 'tenant')
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'tenant', 'status', 'priority', 'assignee', 'due_date')
    list_filter = ('status', 'priority', 'tenant')
