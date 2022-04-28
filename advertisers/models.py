from django.db import models
from core.models import TimeStamp

# Create your models here.
class advertiser_info(TimeStamp):
    advertiser_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=15, default='')
