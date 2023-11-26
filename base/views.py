from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Hello, home.")

def about(request):
    return HttpResponse("Hello, ridwan")