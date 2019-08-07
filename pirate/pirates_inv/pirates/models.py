from django.db import models

# Create your models here.

class Location(models.Model):
    building = models.CharField(db_column='Building',  max_length=255)
    room = models.CharField(db_column='Room', max_length=255)

    class Meta:
        db_table = 'Location'
        unique_together = (('building', 'room'),)


class Vendor(models.Model):
    vendor_name = models.CharField(db_column='Vendor', primary_key=True, max_length=255)

    class Meta:
        db_table = 'vendor'

    def __str__(self):
        return self.vendor_name


