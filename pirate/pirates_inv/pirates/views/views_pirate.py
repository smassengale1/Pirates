from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.views import View
from pirates.models import *
from django.http import Http404



# Create your views here.

decorators = [never_cache, login_required, permission_required('is_superuser', raise_exception=True)]



@login_required()
def dashboard(request):

    user = request.user
    title = 'District Technology'

    if user.is_superuser:
        userType = 'Admin'
        page_temp = 'pirates/dashboards/admin_dashboard.html'
    else:
        userType = 'Guest'
        page_temp = 'pirates/landing_pages/unauth_user.html'

    context = {
        'user': str(user).title(),
        'page_title': title,
    }

    return render(request, page_temp, context)



