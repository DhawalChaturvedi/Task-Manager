from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import AddMemberForm, ProjectForm
from .mixins import ProjectAdminRequired, ProjectMemberRequired
from .models import Project, ProjectMember


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user).distinct()


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        ProjectMember.objects.create(project=self.object, user=self.request.user, role='admin')
        return response

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDetailView(ProjectMemberRequired, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        membership = ProjectMember.objects.get(project=self.object, user=self.request.user)
        ctx['members'] = self.object.members.select_related('user')
        ctx['add_member_form'] = AddMemberForm()
        ctx['user_role'] = membership.role
        ctx['is_admin'] = membership.role == 'admin'
        ctx['tasks'] = self.object.tasks.select_related('assigned_to').order_by('-created_at')
        return ctx


class ProjectUpdateView(ProjectAdminRequired, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(ProjectAdminRequired, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')


class AddMemberView(ProjectAdminRequired, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            role = form.cleaned_data['role']
            _, created = ProjectMember.objects.get_or_create(
                project=project, user=user, defaults={'role': role}
            )
            if not created:
                messages.warning(request, f'{user.username} is already a member.')
            else:
                messages.success(request, f'{user.username} added as {role}.')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
        return redirect('project_detail', pk=pk)


class RemoveMemberView(ProjectAdminRequired, View):
    def post(self, request, pk, uid):
        if request.user.pk == uid:
            messages.error(request, "You can't remove yourself.")
            return redirect('project_detail', pk=pk)
        ProjectMember.objects.filter(project_id=pk, user_id=uid).delete()
        return redirect('project_detail', pk=pk)
