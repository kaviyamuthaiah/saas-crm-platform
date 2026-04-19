"""
projects/forms.py
"""
from django import forms
from apps.projects.models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'status', 'owner', 'start_date', 'due_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, tenant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tenant:
            # Only show users from the same tenant as assignable owners
            self.fields['owner'].queryset = tenant.members.filter(is_active=True)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'status', 'priority', 'assignee', 'due_date')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, tenant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tenant:
            self.fields['assignee'].queryset = tenant.members.filter(is_active=True)
            self.fields['project'].queryset = Project.objects.filter(tenant=tenant)
