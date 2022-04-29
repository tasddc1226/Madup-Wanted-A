from django.db import models
from core.models import TimeStamp
from advertisers.models import advertiser_info

# Create your models here.
class ad_info(TimeStamp):
    uid = models.CharField(max_length=100, primary_key=True)
    advertiser = models.ForeignKey(advertiser_info,max_length=100, on_delete=models.CASCADE)
    media = models.CharField(max_length=100)
    
    

class result_data_set(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser = models.ForeignKey(advertiser_info,max_length=100, on_delete=models.CASCADE)
    uid = models.ForeignKey(ad_info ,max_length=100, on_delete=models.CASCADE)
    media = models.CharField(max_length=100)
    date = models.DateTimeField()
    cost = models.PositiveIntegerField(default=0)
    impression = models.IntegerField(default=0)
    click = models.PositiveIntegerField(default=0)
    conversion = models.IntegerField(default=0)
    cv = models.IntegerField(default=0)
    
    class Meta:
       indexes = [
            models.Index(fields=['advertiser','date']),
            models.Index(fields=['media',]),
       ]