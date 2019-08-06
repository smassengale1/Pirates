from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
# Create your views here.

def index(request):
    page_temp = 'pirates/main.html'
    return render(request, page_temp)