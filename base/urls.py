from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('github-activity/', views.github_activity, name='github-activity'),
    path('project/', views.project, name='project'),
    path('certificate/', views.certificate, name='certificate'),
    path('about/', views.about, name='about'),
]