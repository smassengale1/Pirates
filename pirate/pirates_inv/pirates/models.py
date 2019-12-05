from django.db import models

# Create your models here.

class Asset(models.Model):
    a_type = models.CharField(db_column='AssetType', max_length=255)
    a_brand = models.CharField(db_column='AssetBrand', max_length=255)
    a_model = models.CharField(db_column='AssetModel', max_length=255)
    a_building = models.CharField(db_column='AssetBuilding', default='Technology', max_length=255)
    a_room = models.CharField(db_column='AssetRoom', default='TBD', max_length=255)
    a_quantity = models.IntegerField (db_column='AssetQuantity')
    a_vendor = models.CharField(db_column='AssetVendor', default = 'N/A', max_length=255)

    class Meta:
        db_table = 'asset'

class VendorID(models.Model):
    v_vendor = models.CharField(db_column='VendorName', max_length = 255)
    v_id = models.CharField(db_column='VendorID', max_length = 255)

    class Meta:
        db_table = 'vendor_name'

class Vendor(models.Model):
    v_vendor = models.CharField(db_column='VendorAssetVendor', max_length=255)
    v_id = models.CharField(db_column='VendorAssetID', max_length=25)
    v_type = models.CharField(db_column='VendorAssetModel', max_length=255)
    v_make = models.CharField(db_column='VendorAssetMake', max_length=225)
    v_model = models.CharField(db_column='VendorAssetType', max_length=255)
    v_quantity = models.IntegerField(db_column = 'VendorAssetQuantity', default = -0)
    v_pm = models.IntegerField(db_column='AssetPurchaseMonth', default = 0)
    v_py = models.IntegerField(db_column='AssetPurchaseYear', default=0)
    v_rm = models.IntegerField(db_column='AssetReplacementMonth', default=0)
    v_ry = models.IntegerField(db_column='AssetReplacementYear', default=0)

    class Meta:
        db_table = 'vendor'



class Location(models.Model):
    location_building = models.CharField(db_column='Building',  max_length=255)
    location_room = models.CharField(db_column='Room', max_length=255, default='temp')

    class Meta:
        db_table = 'location'
        unique_together = (('location_building', 'location_room'),)



