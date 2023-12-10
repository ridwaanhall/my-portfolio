from django.urls import path
from . import views
# from django.conf.urls.static import static
# from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('github-activity/', views.github_activity, name='github-activity'),
    path('project/', views.project, name='project'),
    path('certificate/', views.certificate, name='certificate'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('playground/', views.playground, name='playground'),
]

# Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)