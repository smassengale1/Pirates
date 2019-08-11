from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.views import View
from pirates.models import *
from django.http import JsonResponse
import json
from django.http import Http404



# Create your views here.

decorators = [never_cache, login_required, permission_required('is_superuser', raise_exception=True)]



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
class vendors(View):
    def get(self, request, *args, **kwargs):
        page_template = 'pirates/elements/vendors.html'
        page_title = 'Dover Technology Vendors'

        v = []
        for v_name in Vendor.objects.all():
            v_id = (Vendor.objects.get(vendor_name=v_name)).vendor_id
            v.append({
                'v_name': v_name,
                'v_id':v_id,
            })

        context = {
            'page_title': page_title,
            'vendors': v,
        }


        return render(request, page_template, context)


    def post(self, request, *args, **kwargs):
        if self.addVendor(request):
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'error': 'No Vulnerabilties Found'})



    def addVendor(self, request):
        vendorName = request.POST.get('vendorName')
        print(request.body)
        return True
        #x = request.POST.get('vendor_name')

