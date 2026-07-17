"""
URL configuration for project_auth_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('', RedirectView.as_view(pattern_name='login'), name='root_redirect'),
]