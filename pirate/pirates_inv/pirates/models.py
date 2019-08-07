from django.db import models

# Create your models here.


class Location(models.Model):
    building = models.CharField(db_column='Building', primary_key= True, max_length=255)
    room = models.CharField(db_column='Room', primary_key=True, max_length=255)

    class Meta:
        db_table = 'Location'
        unique_together = (('building', 'room'),)


class Vendor(models.Model):
    vendor_name = models.CharField(db_column='Vendor', max_length=255):

    class Meta:
        db_table = 'vendor'


