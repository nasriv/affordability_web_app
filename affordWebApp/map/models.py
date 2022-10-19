import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class fipsCode(models.Model):
    fips = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    countyName = models.CharField(max_length=255)

class statePop(models.Model):
    fips = models.CharField(max_length=255)
    popest2021 = models.IntegerField()