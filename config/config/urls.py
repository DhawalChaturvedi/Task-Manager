from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from apps.accounts.dashboard_view import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.accounts.urls')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('projects/', include('apps.projects.urls')),
    path('', include('apps.tasks.urls')),
    path('', RedirectView.as_view(url='/auth/login/', permanent=False)),
]
