from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('github-activity/', views.github_activity, name='github-activity'),
    path('project/', views.project, name='project'),
    path('certificate/', views.certificate, name='certificate'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('playground/', views.playground, name='playground'),
    
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('comingsoon/', views.comingSoon, name='comingsoon'),
    re_path(r'^.*/$', views.errorPage, name='error'),
]