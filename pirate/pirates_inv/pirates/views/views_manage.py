from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.views import View
from pirates.models import *
from django.http import JsonResponse, HttpResponse
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


@method_decorator(decorators, name='dispatch')
class assets(View):
    def get(self, request, *args, **kwargs):
        page_template = 'pirates/elements/assets.html'
        page_title = 'Dover Technology Assets'

        devices = []
        deviceCount = []  #Holds Device && Device Count
        assetBuildings = []

        #Get the Asset Types
        assetType = Asset.objects.order_by().values('a_type').distinct()
        assetBuilding = Asset.objects.order_by().values('a_building').distinct()

        for types in assetType:
            for colName, asset in types.items():
                assetCount = Asset.objects.filter(a_type = asset).values('a_type').count()
                buildingCount = []
                for building in assetBuilding:
                    for colName, loc in building.items():
                        locationsCount = Asset.objects.filter(a_building = loc).filter(a_type = asset).values('a_building').count()



                        buildingCount.append({
                            'building' : loc,
                            'count' : locationsCount
                        })

                assetBuildings.append({
                    str(asset): buildingCount
                })

                deviceCount.append({
                    'type': asset,
                    'count' : assetCount
                })

            roomCount = self.getLocations()
            roomDevices = self.getAssetLocations()

        context = {
            'types': devices,
            'deviceCount': deviceCount,
            'roomCount': roomCount,
            'locations': assetBuildings,
            'roomDevices': roomDevices,
        }

        return render(request, page_template, context)


    def post(self, request, *args, **kwargs):
        pass



    def getLocations(self):
        distictRooms = []

        districtLocations = Location.objects.order_by().values('location_building').distinct()



        for loc in districtLocations:
            for colName, building in loc.items():
                roomCount = Location.objects.filter(location_building = building).values('location_room').count()
                locationRooms = Location.objects.filter(location_building = building).values('location_room')

                r = []
                for rooms in locationRooms:
                    r.append(rooms)

                distictRooms.append({
                    str(building): r,
                })



        return distictRooms


    def getAssetLocations(self):

        districtBuildings = Asset.objects.order_by().values('a_building').distinct()
        assetBreakdown = []


        buildingSet = []
        for b in districtBuildings:
            for colName, building in b.items():
                districtDevices = Asset.objects.filter(a_building=building).values('a_type')
                typeSet = []
                for t in districtDevices:
                    for colNam, type in t.items():
                        districtModels = Asset.objects.filter (a_building=building).filter(a_type=type).values('a_brand', 'a_model').distinct()
                        modelSet = []
                        for m in districtModels:
                            districtRooms = Asset.objects.filter(a_building=building).filter(a_model=m['a_model'])
                            roomSet = []

                            totalDict = districtRooms.aggregate(Sum('a_quantity'))
                            totalRooms = districtRooms.values('a_room').count





                            deviceSet=[]
                            for set in districtRooms.values('a_room', 'a_quantity'):
                                deviceSet.append({
                                    'room': set['a_room'],
                                    'quantity': set['a_quantity'],
                                })


                            modelSet.append({
                               'model': m['a_model'],
                               'brand': m['a_brand'],
                               'deviceCount': totalDict['a_quantity__sum'],
                               'roomCount': totalRooms,
                               'roomLocations': deviceSet
                            })





                            roomSet.append({
                                m['a_model'] : deviceSet,
                            })

                        typeSet.append({
                            type:modelSet,
                            'rooms': roomSet
                        })

                buildingSet.append({
                    building:typeSet
                })





        assetBreakdown.append({
            'building' : buildingSet
        })



        return assetBreakdown





##############################Delete############################################
@method_decorator(decorators, name='dispatch')
class deviceBreakDown(View):
    def get(self, request, *args, **kwargs):
        page_template = 'pirates/elements/asset_breakdown.html'
        return render(request, page_template)


    def post(self, request, *args, **kwargs):
        page_template = 'pirates/elements/asset_breakdown.html'

        print(request.POST)

        #deviceInfo = self.getInfo(deviceType)


        return render(request, 'pirates/elements/asset_breakdown.html')


    def getInfo(self, deviceType):
        locCount = []

        districtLoc = Asset.objects.order_by().values('a_building').distinct()

        for qSet in districtLoc:
            for colName, building in qSet.items():
                deviceCount = Asset.objects.filter(a_building = building, a_type = deviceType).values().count()
                print(deviceCount)

            locCount.append({
                'building': building,
                'count' : deviceCount
            })

        return deviceCount

