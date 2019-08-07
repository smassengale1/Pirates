from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
# Create your views here.


def dashboard(request):
    page_temp = 'pirates/dashboard.html'
    return render(request, page_temp)