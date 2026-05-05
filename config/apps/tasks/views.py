from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.projects.mixins import ProjectAdminRequired, ProjectMemberRequired
from apps.projects.models import Project, ProjectMember
from .forms import TaskForm
from .models import Task


def _is_project_admin(user, project):
    return ProjectMember.objects.filter(project=project, user=user, role='admin').exists()


class TaskCreateView(ProjectMemberRequired, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = TaskForm(project=project)
        html = render_to_string(
            'tasks/task_form_partial.html',
            {'form': form, 'project': project},
            request=request,
        )
        return HttpResponse(html)

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            tasks = project.tasks.select_related('assigned_to').order_by('-created_at')
            html = render_to_string(
                'tasks/task_list_partial.html',
                {'tasks': tasks, 'project': project, 'user': request.user,
                 'is_admin': _is_project_admin(request.user, project)},
                request=request,
            )
            return HttpResponse(html)
        html = render_to_string(
            'tasks/task_form_partial.html',
            {'form': form, 'project': project},
            request=request,
        )
        return HttpResponse(html)


class TaskUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if not _is_project_admin(request.user, task.project):
            raise PermissionDenied
        form = TaskForm(instance=task, project=task.project)
        html = render_to_string(
            'tasks/task_form_partial.html',
            {'form': form, 'project': task.project, 'task': task},
            request=request,
        )
        return HttpResponse(html)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if not _is_project_admin(request.user, task.project):
            raise PermissionDenied
        form = TaskForm(request.POST, instance=task, project=task.project)
        if form.is_valid():
            form.save()
            tasks = task.project.tasks.select_related('assigned_to').order_by('-created_at')
            html = render_to_string(
                'tasks/task_list_partial.html',
                {'tasks': tasks, 'project': task.project, 'user': request.user,
                 'is_admin': True},
                request=request,
            )
            return HttpResponse(html)
        html = render_to_string(
            'tasks/task_form_partial.html',
            {'form': form, 'project': task.project, 'task': task},
            request=request,
        )
        return HttpResponse(html)


class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if not _is_project_admin(request.user, task.project):
            raise PermissionDenied
        project = task.project
        task.delete()
        tasks = project.tasks.select_related('assigned_to').order_by('-created_at')
        html = render_to_string(
            'tasks/task_list_partial.html',
            {'tasks': tasks, 'project': project, 'user': request.user, 'is_admin': True},
            request=request,
        )
        return HttpResponse(html)


class TaskStatusView(ProjectMemberRequired, View):
    """HTMX endpoint — cycles task status and returns updated row."""
    STATUS_CYCLE = {'todo': 'in_progress', 'in_progress': 'done', 'done': 'todo'}

    def post(self, request, pk):
        # pk here is project pk from URL; task pk is in POST body
        task_pk = request.POST.get('task_pk')
        task = get_object_or_404(Task, pk=task_pk, project_id=pk)
        task.status = self.STATUS_CYCLE[task.status]
        task.save(update_fields=['status'])
        is_admin = _is_project_admin(request.user, task.project)
        html = render_to_string(
            'tasks/task_row_partial.html',
            {'task': task, 'project': task.project, 'is_admin': is_admin},
            request=request,
        )
        return HttpResponse(html)
