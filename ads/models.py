from django.db import models
from core.models import TimeStamp
from advertisers.models import advertiser_info

# Create your models here.
class ad_info(TimeStamp):
    uid = models.CharField(max_length=100, primary_key=True)
    advertiser = models.ForeignKey(advertiser_info,max_length=100, on_delete=models.CASCADE)
    media = models.CharField(max_length=100)
    
    

class result_data_set(models.Model):
    advertiser = models.ForeignKey(advertiser_info,max_length=100, on_delete=models.CASCADE)
    uid = models.ForeignKey(ad_info ,max_length=100, primary_key=True, on_delete=models.CASCADE)
    media = models.CharField(max_length=100)
    date = models.DateTimeField()
    cost = models.IntegerField()
    impression = models.IntegerField()
    click = models.IntegerField()
    conversion = models.IntegerField()
    cv = models.IntegerField()
    
    class Meta:
       indexes = [
            models.Index(fields=['advertiser','date']),
            models.Index(fields=['media',]),
       ]