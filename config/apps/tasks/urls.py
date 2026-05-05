from django.urls import path
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView, TaskStatusView

urlpatterns = [
    path('projects/<int:pk>/tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('projects/<int:pk>/tasks/status/', TaskStatusView.as_view(), name='task_status'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
