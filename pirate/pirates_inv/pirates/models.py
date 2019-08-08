from django.db import models

# Create your models here.

class Location(models.Model):
    building = models.CharField(db_column='Building',  max_length=255)
    room = models.CharField(db_column='Room', max_length=255)

    class Meta:
        db_table = 'location'
        unique_together = (('building', 'room'),)


class Vendor(models.Model):
    vendor_name = models.CharField(db_column='Vendor', primary_key=True, max_length=255)
    vendor_id = models.CharField(db_column='VendorID', unique=True, max_length=255)

    class Meta:
        db_table = 'vendor'

    def __str__(self):
        return self.vendor_name


class Asset(models.Model):
    asset_type= models.CharField(db_column='AssetType', max_length=255)
    asset_brand= models.CharField(db_column='AssetBrand', max_length=255)
    asset_model= models.CharField(db_column='AssetModel', max_length=255)
    asset_tag= models.CharField(db_column='AssetTag', unique=True, max_length=255)
    asset_sn= models.CharField(db_column='AssetSN', unique=True, max_length=255)
    asset_vendor= models.CharField(db_column='AssetVendor', default='N/A', max_length=255)
    asset_condition= models.CharField(db_column='AssetCondition', null=True, max_length=255)
    asset_notes = models.TextField(db_column='AssetNotes', null=True)
    asset_canbe_checked= models.BooleanField(db_column='AssetStatus', default=False)

    class Meta:
        db_table= 'asset'


