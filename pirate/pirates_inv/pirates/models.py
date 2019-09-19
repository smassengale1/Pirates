from django.db import models

# Create your models here.

class Asset(models.Model):
    asset_type = models.CharField(db_column='AssetType', max_length=255)
    asset_brand = models.CharField(db_column='AssetBrand', max_length=255)
    asset_model = models.CharField(db_column='AssetModel', max_length=255)
    asset_building = models.CharField(db_column='AssetBuilding', default='Technology', max_length=255)
    asset_room = models.CharField(db_column='AssetRoom', default='TBD', max_length=255)
    asset_quantity = models.IntegerField (db_column='AssetQuantity')

    class Meta:
        db_table = 'asset'



class Vendor(models.Model):
    vendor_asset_type = models.CharField(db_column='VendorAssetType', max_length=255)
    vendor_asset_brand = models.CharField(db_column='VendorAssetBrand', max_length=255)
    vendor_asset_model = models.CharField(db_column='VendorAssetModel', max_length=255)
    vendor_asset_vendor = models.CharField(db_column='VendorAssetVendor', max_length=255)
    vendor_asset_quantity_bought = models.IntegerField (db_column='VendorAssetQuantityBought', default= -0)
    vendor_asset_purchase_month = models.IntegerField(db_column='VendorAssetPurchaseMonth', null = True)
    vendor_asset_purchase_year = models.IntegerField(db_column='VendorAssetPurchaseYear', null=True)
    vendor_asset_replacement_month = models.IntegerField(db_column='VendorAssetReplacementMonth', default = 0)
    vendor_asset_replacement_year = models.IntegerField(db_column='VendorAssetReplacementYear', default = 0)

    class Meta:
        db_table = 'vendor'


class Location(models.Model):
    location_building = models.CharField(db_column='Building',  max_length=255)
    location_room = models.CharField(db_column='Room', max_length=255)

    class Meta:
        db_table = 'location'
        unique_together = (('location_building', 'location_room'),)



