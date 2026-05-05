from django.urls import path
from .views import (
    ProjectListView, ProjectCreateView, ProjectDetailView,
    ProjectUpdateView, ProjectDeleteView, AddMemberView, RemoveMemberView,
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:pk>/members/add/', AddMemberView.as_view(), name='project_add_member'),
    path('<int:pk>/members/<int:uid>/remove/', RemoveMemberView.as_view(), name='project_remove_member'),
]
