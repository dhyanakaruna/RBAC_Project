from django import forms
from .models import User, Role

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'roles']
        widgets = {
            'password': forms.PasswordInput(),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']