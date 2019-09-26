from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.views import View
from pirates.models import *
from django.http import JsonResponse
import json
from django.db.models import Sum
from django.http import Http404


decorators = [never_cache, login_required, permission_required('is_superuser', raise_exception=True)]


@method_decorator(decorators, name='dispatch')
class vendors(View):
    def get(self, request, *args, **kwargs):
        page_template = 'pirates/elements/vendors.html'
        page_title = 'Dover Technology Vendors'




        model_list = []
        vendor_list = []
        v_stats = []


        device_info = []

        districtDevices = Vendor.objects.order_by().values('v_type').distinct()


        # The first two loops gets Asset Types [Projector, Chromebook, Laptop, ect...]
        for devices in districtDevices:
            model_list = []
            for colName, assetType in devices.items():
                districtModels = Vendor.objects.filter(v_type=assetType).values('v_model').distinct()
                vendorCount = Vendor.objects.filter(v_type = assetType).values('v_vendor').distinct().count()

                vendor_list.append({
                    'device' : assetType,
                    'count'  : vendorCount,
                })

                #models_info = []
                for models in districtModels:
                    models_info = []
                    for colName, assetModel in models.items():

                        districtVendors = Vendor.objects.filter(v_model = assetModel).values('v_vendor', 'v_brand','v_qb', 'v_pm', 'v_py', 'v_rm', 'v_ry')



                        for vendors in districtVendors:
                            device_info = {
                                'v_type': assetType,
                                'v_model': assetModel,
                                'v_brand': vendors['v_brand'],
                                'v_name': vendors['v_vendor'],
                                'v_qb': vendors['v_qb'],
                                'v_pm': vendors['v_pm'],
                                'v_py': vendors['v_py'],
                                'v_rm': vendors['v_rm'],
                                'v_ry': vendors['v_ry'],

                            }

                            models_info.append(device_info)

                        model_list .append(models_info)

                v_stats.append({
                    str(assetType): model_list
                })



        for item in v_stats:
            for type, col in item.items():
                print(type)
                for x in col:
                    print('i')


        context = {
            'page_title': page_title,
            'vendors': v_stats,
            'vendorCount': vendor_list,
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



@method_decorator(decorators, name='dispatch')
class locations(View):
    def get(self, request, *args, **kwargs):
        page_template = 'pirates/elements/locations.html'
        page_title = 'Dover Locations'

        buildings_list = []
        rooms_list = []

        districtLocations = Location.objects.order_by().values('location_building').distinct()



        for loc in districtLocations:
            for colName, building in loc.items():
                roomCount = Location.objects.filter(location_building = building).values('location_room').count()
                locationRooms = Location.objects.filter(location_building = building).values('location_room')

                r = []
                for rooms in locationRooms:
                    r.append(rooms)

                rooms_list.append({
                    str(building): r,
                })

                buildings_list.append({
                    'location': building,
                    'roomCount': roomCount,
                })



        context = {
            'locations' : buildings_list,
            'rooms' : rooms_list,
            'roomRange' : range(len(rooms_list)),
        }



        return render(request, page_template, context)
