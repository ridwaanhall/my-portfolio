from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/<str:pk>', views.about, name='about'),
]