from django.db import models

# Create your models here.

class Requests(models.Model):
    ASSET_TYPE = (
        ('LAPTOP','LAPTOP'),
        ('TRAVEL_BAG','TRAVEL_BAG'),
        ('PACKAGE','PACKAGE')
    )
    SENSITIVE_TYPE = (
        ('HIGHLY_SENSITIVE','HIGHLY_SENSITIVE'),
        ('SENSITIVE','SENSITIVE'),
        ('NORMAL','NORMAL')
    )
    requesterid = models.IntegerField(max_length=200)                       ## id of the user requester
    assettype = models.CharField(max_length=200,choices=ASSET_TYPE)         ## type of asset
    numberassets = models.PositiveIntegerField(max_length=200)              ## number of assets
    dateandtime = models.DateField()
    fromplace = models.CharField(max_length=200)
    toplace = models.CharField(max_length=200)
    todeliverperson = models.CharField(max_length=200)
    deliverby = models.IntegerField(blank=True, null=True)          ## id of person deliveing
    packagesensitivity = models.CharField(max_length=200,choices=SENSITIVE_TYPE)
    status = models.CharField(max_length=200,default = "PENDING",blank=True, null=True)


class Rides(models.Model):
    travel_medium = (
        ('BUS','BUS'),
        ('CAR','CAR'),
        ('TRAIN','TRAIN')
    )
    riderid = models.CharField(max_length=200)
    fromplace = models.CharField(max_length=200)
    toplace = models.CharField(max_length=200)
    dateandtime = models.DateField()
    travelmedium = models.CharField(max_length=200,choices=travel_medium)
    quantity = models.PositiveIntegerField(max_length=200)
