from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views import View

from .models import ProjectMember


class ProjectMemberRequired(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(ProjectMember, project_id=kwargs['pk'], user=request.user)
        return super().dispatch(request, *args, **kwargs)


class ProjectAdminRequired(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        membership = get_object_or_404(ProjectMember, project_id=kwargs['pk'], user=request.user)
        if membership.role != 'admin':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
