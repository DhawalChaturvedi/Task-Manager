from django import forms
from django.contrib.auth import get_user_model

from .models import Project

User = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')


class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=150)
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('member', 'Member')])

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('No user with that username exists.')
