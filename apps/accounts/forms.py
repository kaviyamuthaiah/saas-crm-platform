"""
accounts/forms.py

Registration and profile forms for the multi-tenant SaaS platform.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.accounts.models import User
from apps.tenants.models import Tenant


class RegisterForm(UserCreationForm):
    """
    Registration form that creates a new Tenant and sets the user as Admin.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'you@company.com'}))
    company_name = forms.CharField(
        max_length=150,
        required=True,
        help_text='Your organisation / company name. A new workspace will be created.',
        widget=forms.TextInput(attrs={'placeholder': 'Acme Inc.'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'company_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Create a new tenant for this user (they become the admin)
        if commit:
            tenant = Tenant.objects.create(name=self.cleaned_data['company_name'])
            user.tenant = tenant
            user.role = User.Role.ADMIN
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Styled login form."""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class UserProfileForm(forms.ModelForm):
    """Allow users to update their own profile."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'avatar')


class InviteUserForm(forms.ModelForm):
    """Tenant admin can invite a new user (same tenant, USER role)."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'role')

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, tenant, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.tenant = tenant
        if commit:
            user.save()
        return user
