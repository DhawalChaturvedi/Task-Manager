from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView

from apps.tasks.models import Task


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_tasks = (
            Task.objects
            .filter(project__members__user=self.request.user)
            .select_related('project', 'assigned_to')
        )
        ctx['overdue'] = user_tasks.filter(
            due_date__lt=date.today()
        ).exclude(status='done').order_by('due_date')

        by_status = {
            row['status']: row['count']
            for row in user_tasks.values('status').annotate(count=Count('id'))
        }
        ctx['count_todo'] = by_status.get('todo', 0)
        ctx['count_in_progress'] = by_status.get('in_progress', 0)
        ctx['count_done'] = by_status.get('done', 0)
        ctx['total'] = sum(by_status.values())
        return ctx
