from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, home.")

def about(request):
    return HttpResponse("Hello, ridwan")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    
]
