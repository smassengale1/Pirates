from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def dashboard(request):

    user = request.user
    title = '%s Dashboard'

    if user.is_superuser:
        userType = 'Admin'
        page_temp = 'pirates/dashboards/admin_dashboard.html'

    elif user.is_staff:
        userType = 'Staff'
        page_temp = 'pirates/dashboards/staff_dashboard.html'
    else:
        userType = 'Student'
        page_temp = 'pirates/dashboards/admin_dashboard.html'

    context = {
        'user': str(user).title(),
        'title': title % userType,
    }

    return render(request, page_temp, context)