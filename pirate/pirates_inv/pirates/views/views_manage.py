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



        device_list = []
        vendor_list = []

        districtDevices = Vendor.objects.order_by().values('vendor_asset_type').distinct()


        # The first two loops gets Asset Types [Projector, Chromebook, Laptop, ect...]
        for devices in districtDevices:
            for colName, assetType in devices.items():
                districtModels = Vendor.objects.filter(vendor_asset_type=assetType).values('vendor_asset_model').distinct()
                for models in districtModels:
                    for colName, assetModel in models.items():
                        districtVendors = Vendor.objects.filter(vendor_asset_model = assetModel).values('vendor_asset_vendor', 'vendor_asset_quantity_bought',
                                                                                                         'vendor_asset_purchase_month', 'vendor_asset_purchase_year',
                                                                                                         'vendor_asset_replacement_month', 'vendor_asset_replacement_year')
                        t = []
                        for vendors in districtVendors:
                            t= {
                                'v_type': assetType,
                                'v_name': vendors['vendor_asset_vendor'],
                                'v_qb': vendors['vendor_asset_quantity_bought'],
                                'v_pm': vendors['vendor_asset_purchase_month'],
                                'v_py': vendors['vendor_asset_purchase_year'],
                                'v_rm': vendors['vendor_asset_replacement_month'],
                                'v_ry': vendors['vendor_asset_replacement_year'],

                            }

                            if assetModel not in model_list:
                                model_list.append(assetModel)
                                device_info['v_model'] = assetModel

                            myDict.append({
                                str(assetType) : t
                            })

        v_stats.append({
            'Chromebook' : Chromebook_dict,
            'Laptop' : Laptop_dict,
            'Desktop': Desktop_dict,
            'Projector': Projector_dict,
            'Document Camera' : documentCam_dict,
            'Smart Board' : smartBoard_dict,
            'Security Camera': securityCam_dict,
            'Misc' : Misc_dict,

        })

        context = {
            'page_title': page_title,
            'vendors': v_stats,
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
