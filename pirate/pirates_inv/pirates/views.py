from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
# Create your views here.

decorators = [never_cache, login_required]

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
        page_temp = 'pirates/dashboards/student_dashboard.html'

    context = {
        'user': str(user).title(),
        'title': title % userType,
    }

    return render(request, page_temp, context)

@method_decorator(decorators, name='dispatch')
class vendors(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pirates/elements/vendors.html')
    def post(selfs, request, *args, **kwargs):
        return render(request)

