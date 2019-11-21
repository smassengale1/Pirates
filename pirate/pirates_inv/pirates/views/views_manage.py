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

        districtVendors = Vendor.objects.order_by().values('v_vendor', 'v_id').distinct()

        vendor_list = [] #gives info about vendors
        vendor_stats = [] #names the cards on webpage


        for v in districtVendors: #v['v_vendor'] && v['v_id']
            districtTypes = Vendor.objects.filter(v_vendor = v['v_vendor'])
            type_list = []
            for t in districtTypes.values('v_type').distinct():
                model_list = []
                for m in districtTypes.filter(v_type = t['v_type']).values('v_model').distinct():
                    date_list = []
                    for d in districtTypes.filter(v_type = t['v_type']).filter(v_model = m['v_model']).values('v_quantity','v_pm', 'v_py', 'v_rm', 'v_ry'):
                        date_list.append(d)

                    model_list.append({
                        m['v_model'] : date_list
                    })

                type_list.append({
                    t['v_type']:model_list
                })

            vendor_list.append({
                v['v_vendor'] : type_list,
            })

            vendor_stats.append({
                'vendor' : v['v_vendor'],
                'id' : v['v_id']
            })


        print(vendor_list)
        context = {
            'page_title': page_title,
            'vendors' : vendor_list,
            'cards' : vendor_stats,
        }


        return render(request, page_template, context)


def add_vendor(request):
    vendor = request.POST.get('vendor', None)
    id = request.POST.get('vendorID', None)

    exist = Vendor.objects.filter(v_vendor = vendor, v_id = id).exists()
    print("Checking if %s(%s) is unique: " % (vendor,id), end='/')
    if(not exist):
        print("Confirmed/")
        print("Adding New Vendor: ", end='/')
        newVendor = Vendor(v_vendor = vendor, v_id = id)
        newVendor.save()
        print("%s(%s) added/" % (vendor, id))
    else:
        print("Failed/")
        print("ABORTING")

    data = { 'exists' : exist }

    return JsonResponse(data, safe=False)

##ADDS NEW DEVICE TO BE TRACKED
def track_device(request):

    device = request.POST.get('device', None).strip()
    exist = deviceType.objects.filter(d_type=device).exists()
    data={'exist': exist}

    if not exist:
        newDevice = deviceType(d_type = device)
        newDevice.save()
    else:
        print('failed')

    return data


###CHANGES DATA IN DB
def update_vendor(request):
    type = request.POST.get('type', None).strip()
    oldName = request.POST.get('oldName', None).strip()
    newName = request.POST.get('newName', None).strip()

    if type == 'device':
        update_vendor_device(oldName, newName)

    data = []
    return JsonResponse(data, safe=False)



def update_vendor_device(oldName, newName):
    exist = deviceType.objects.filter(d_type=newName).exists()

    data={
        'exist':exist,
        'isNull':False
    }

    if not exist:
        if newName != '':
            v = deviceType.objects.filter(d_type=oldName)

            print("Renaming %s ----> %s" % (oldName, newName))
            for i in v:
                i.d_type= newName
                i.save()
            print("Device Type has been changed.")

            """
            print('Updating Devices where Type was %s to %s' % (oldName, newName))
            for i in a:
                i.a_building = newName
                i.save()
            print("Types have been reassigned")
            
            """
        else:
            data['isNull'] = True
    else:
        print("UPDATE ERROR: Name already exist")




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

    if type == 'room':
        print("Adding a New Room")
        room = request.POST.get('room', None).strip()
        data = addRoom(building, room)

    else:
        print("Adding a New Building")
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
        print("Error: %s already exists in District Building" % building)


    return data



def addRoom(building, room):
    exist = Location.objects.filter(location_building = building, location_room = room).exists()


    data = {'exist' : exist}

    if not exist:
        if room != '':
            data['isNull'] = False

            print("Attempting to add %s[%s]" % (building, room))

            record = Location(location_building = building, location_room = room)
            record.save()

            print("Successfully added --> %s[%s]" % (building, room))

        else:
            print("Error: Cannot add Null Entry")
            data['isNull'] = True


    else:
        print("Error: %s[%s] already exists." % (building, room))






    return data






def update_building(request):
    oldName = request.POST.get('oldRoom', None).strip()
    newName = request.POST.get('newRoom', None).strip()
    type = request.POST.get('type', None).strip()


    if type == 'room':
        print('\n--------------------Modifying Room--------------------')
        building = request.POST.get('building', None).strip()
        data = updateRoom(oldName, newName, building)
        print('----------------------------------------------------')

    else:
        print('\n--------------------Modifying Building--------------------')
        data = updateBuilding(oldName, newName)
        print('---------------------------------------------------------')



    return JsonResponse(data, safe=False)

def updateBuilding(oldName, newName):
    exist = Location.objects.filter(location_building = newName).exists()
    data = {'exist' : exist}

    print("Confirming %s is unique: " % (newName), end='/')
    if not exist:
        if newName != '':
            print("Confirmed/")
            data['isNull'] = False
            l = Location.objects.filter(location_building=oldName)
            a = Asset.objects.filter(a_building = oldName)

            print("Renaming %s ----> %s" % (oldName, newName))
            for i in l:
                i.location_building = newName
                i.save()
            print("Room has been changed.")

            print('Updating Rooms where Building was %s to %s' % (oldName, newName))
            for i in a:
                i.a_building = newName
                i.save()
            print("Rooms have been reassigned")
        else:
            print("UPDATE ERROR: Name can not be null")
            data['isNull'] = True


    else:
        print("%s Already Exist" % newName)

    return data

def updateRoom(oldName, newName, building):
    exist = Location.objects.filter(location_building = building, location_room = newName).exists()
    data = {'exist':exist}

    print("Confirming %s[%s] is unique:" % (building, newName) , end='  ')
    if not exist:
        if newName != '':
            data['isNull'] = False

            print("Confirmed.  ")
            l = Location.objects.filter(location_building = building, location_room = oldName)
            a = Asset.objects.filter(a_building = building, a_room = oldName)

            print("Renaming %s[%s] ----> %s[%s]:" % (building, oldName, building, newName), end = "  ")
            for i in l:
                i.location_room = newName
                i.save()
            print("Completed  ")

            print("Reassigning assets tied to %s[%s} ----> %s[%s]:" % (building, oldName, building, newName), end=" ")
            for assets in a:
                assets.a_room = newName
                assets.save()
            print("Completed  ")
        else:
            print("\n\nUPDATE ERROR: New name cannot be null")

            data['isNull'] = True
    else:
        print("Failed  ")
        print("\n\nUPDATE ERROR: %s[%s] is not unique." % (building, newName))
        print("aborting...")


    return data




def remove_location(request):
    area = request.POST.get('area', None).strip()
    type = request.POST.get('type', None)
    building = request.POST.get('roomBuilding', None).strip()

    print("-----Removing Location Module-----")

    if type == 'building':
        print("Location Type: Building")
        data = removeBuilding(area)

    else:
        print("Location Type: Room")
        data = removeRoom(building, area)


    return JsonResponse(data, safe=False)



def removeBuilding(building):
    print('Confirming %s is in Database' % building)
    l = Location.objects.filter(location_building=building)
    a = Asset.objects.filter(a_building=building)
    data = {}

    if l.exists():
        print("%s Confirmed" % building)
        data['exist'] = True

        if a.count() != 0:
            print("Reassigning Assets tied to <%s> --> Technology Office" % building)
            building = 'Technology Office'
            if not Location.objects.filter(location_building = building).exists():
                    print('Technology Office not found; Creating Technology Office')
                    addBuilding(building)


            for i in a:
                i.a_building = building
                i.a_room = 'temp'
                i.save()


        for loc in l:
            loc.delete()

    if l.exists():
        data['data'] = False


    return data



def removeRoom(building, room):
    print("\nConfirming %s <%s>" % (building, room))
    l = Location.objects.filter(location_building=building, location_room=room)
    a = Asset.objects.filter(a_building=building, a_room=room)
    data = {}

    if l.exists():
        print("%s <%s> confirmed" % (building, room))
        data['exist'] = True
        if a.count() > 0:
            print("Reassigning Assets tied to %s <%s>" % (building, room))
            if not Location.objects.filter(location_building = building, location_room = 'temp').exists():
                addRoom('temp', building)
                print('Devices Reassigned to %s <temp>\n\n' % building)


            for i in a:
                i.a_building = building
                i.a_room = 'temp'
                i.save()

    else:
        print("LOCATION NOT FOUND: %s <%s> was not found; aborting.\n\n" % (building, room))


    for loc in l:
        loc.delete()

    if l.exists():
        data = {
            'exist': False
        }


    return data





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

