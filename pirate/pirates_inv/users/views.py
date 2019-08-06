from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    return render(request, 'users/register.html', {'form': form})
# Create your views here.
