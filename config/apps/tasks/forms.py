from django.contrib.auth import get_user_model
from django import forms
from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'assigned_to', 'status', 'priority', 'due_date')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            member_ids = project.members.values_list('user_id', flat=True)
            self.fields['assigned_to'].queryset = User.objects.filter(pk__in=member_ids)
