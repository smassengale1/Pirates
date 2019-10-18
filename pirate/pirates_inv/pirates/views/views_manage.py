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




def validate_building(request):
    building = request.POST.get('building', None).strip()
    type = request.POST.get('type', None)

    if type == 'new_room':
        room = request.POST.get('room', None).strip()
        data = addRoom(building, room)

    else:
        data = addBuilding(building)

    return JsonResponse(data, safe=False)



def addBuilding(building):
    exist = Location.objects.filter(location_building = building).exists()

    data = {'exist' : exist}

    if not exist:
        if building != '':
            data['isNull'] = False

            print("Attempting to add <%s> to District Buildings" % building)

            record = Location(location_building = building)
            record.save()

            print("Successfully added <%s> to District Buildings" % building)

        else:
            print("Error: Cannot add Null Entry")
            data['isNull'] = True

    else:
        print("Error: %s already exists in District Building")


    return data



def addRoom(building, room):
    exist = Location.objects.filter(location_building = building, location_room = room).exists()

    data = {'exist' : exist}

    if not exist:
        if room != '':
            data['isNull'] = False

            print("Attempting to add <%s>: <%s>" % (building, room))

            record = Location(location_building = building, location_room = room)
            record.save()

            print("Successfully add --> <%s>: <%s>" % (building, room))

        else:
            print("Error: Cannot add Null Entry")
            data['isNull'] = True


    else:
        print("Error: %s: %s already exists." % (building, room))



    return data








def update_building(request):
    oldName = request.POST.get('oldName', None).strip()
    newName = request.POST.get('newName', None).strip()

    exist = Location.objects.filter(location_building = newName).exists()

    if not exist:
        l = Location.objects.filter(location_building=oldName)
        a = Asset.objects.filter(a_building = oldName)

        print('Updating Location Building Name from %s to %s' % (oldName, newName))
        for i in l:
            i.location_building = newName
            i.save()

        print('Updating Assets where Building was %s to %s' % (oldName, newName))
        for i in a:
            i.a_building = newName
            i.save()

    else:
        print("%s Already Exist" % newName)


    data = {
        'exist':exist
    }

    return JsonResponse(data, safe=False)


def remove_building(request):
    area = request.POST.get('area', None).strip()
    type = request.POST.get('type', None)
    building = request.POST.get('roomBuilding', None).strip()


    if type == 'building':
        print('Confirming %s is a Building' % area)
        l = Location.objects.filter(location_building=area)
        a = Asset.objects.filter(a_building=area)

    else:
        print('Confirming %s: %s is in Database' % (building, area))
        building = request.POST.get('roomBuilding', None)
        l = Location.objects.filter(location_building=building, location_room=area)
        a = Asset.objects.filter(a_building=building, a_room=area)



    if l.exists():
        print('%s confirmed' % area)
        data = {
            'exist': True
        }

        if a.count() != 0:
            print("Devices still assigned to %s" % area)
            if type == 'building':
                if not Location.objects.filter(location_building = 'Technology Office').exists() :
                    print('Creating Temporary Storage')
                    validate_building('Technology Office')

                    building = 'Technology Office'

            else:
                if not Location.objects.filter(location_building = building, location_room = 'temp').exists():
                    print('Creating Temporary Storage in %s: temp' % (building))
                    #need to make validate rooms ready for this


        for i in a:
            i.a_building = building
            i.a_room = 'temp'
            i.save()

    for loc in l:
        loc.delete()



    if l.exists():
        data = {
            'exist': False
        }



    return JsonResponse(data, safe=False)


@method_decorator(decorators, name='dispatch')
class assets(View):
    def get(self, request, *args, **kwargs):
        page_template = 'pirates/elements/assets.html'
        page_title = 'Dover Technology Assets'

        deviceCount = []  #Holds Device && Device Count
        assetBuildings = []
        assetList = []

        #Get the Asset Types
        assetType = Asset.objects.order_by().values('a_type').distinct()
        assetBuilding = Asset.objects.order_by().values('a_building').distinct()

        for types in assetType:
            for colName, asset in types.items():
                assetList.append(asset)
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


        assetRooms = self.getAssetRooms()

        vendors = self.getVendors(assetList)



        context = {
            'deviceCount': deviceCount,
            'roomCount': roomCount,
            'locations': assetBuildings,
            'roomDevices': roomDevices,
            'assetRooms' : assetRooms,
            'vendors':vendors,

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
                    })

                buildingSet.append({
                    building:typeSet
                })





        assetBreakdown.append({
            'building' : buildingSet
        })



        return assetBreakdown




    def getAssetRooms(self):
        assetRooms = []
        districtBuildings = Asset.objects.order_by().values('a_building').distinct()
        for buildings in districtBuildings:
            buildingList=[]
            for colName, building in buildings.items():
                districtTypes = Asset.objects.filter(a_building=building).values('a_type').distinct()
                typeList = []
                for t in districtTypes:
                    districtModels = Asset.objects.filter(a_building=building).filter(a_type=t['a_type']).values('a_model').distinct()
                    modelList = []
                    for m in districtModels:
                        districtRooms = Asset.objects.filter(a_building=building).filter(a_type=t['a_type']).filter(a_model=m['a_model']).values('a_room', 'a_quantity')
                        roomList = []
                        for r in districtRooms:
                            roomList.append({
                                'room': r['a_room'],
                                'quantity' : r['a_quantity']
                            })

                        modelList.append({
                            m['a_model']:roomList
                        })

                    typeList.append({
                        t['a_type'] : modelList
                    })

                buildingList.append({
                    building : typeList
                })

            assetRooms.append({
                'assetRooms': buildingList
            })

        return assetRooms


    def getVendors(self, assetTypes):
        districtVendors = Vendor.objects.order_by().values('v_vendor').distinct()
        vendors = []
        for type in assetTypes:
            vendorList = []
            for v in districtVendors:
                districtPD = Vendor.objects.filter(v_type=type).filter(v_vendor=v['v_vendor']).values('v_pm', 'v_py')
                if districtPD.count() != 0:
                    pdList = []
                    for pd in districtPD:
                        pdList.append({
                            'month' : pd['v_pm'],
                            'year' : pd['v_py']
                        })

                    vendorList.append({
                        v['v_vendor'] : pdList
                    })

            vendors.append({
                type : vendorList
            })

        return vendors




















                    
                        

                        


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

