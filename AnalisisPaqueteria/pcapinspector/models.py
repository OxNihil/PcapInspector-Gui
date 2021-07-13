from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class PcapInfo(models.Model):
    frame_number = models.IntegerField(primary_key=True)
    frame_time = models.CharField(max_length=50)
    eth_src = models.CharField(max_length=20,null=True,blank=True)
    eth_dst = models.CharField(max_length=20,null=True,blank=True)
    ip_src = models.CharField(max_length=16,null=True, blank=True)
    ip_dst = models.CharField(max_length=16,null=True,blank=True)
    src_port = models.IntegerField(null=True, blank=True)
    dst_port = models.IntegerField(null=True, blank=True)
    ttl = models.IntegerField(null=True,blank=True)
    protocol = models.CharField(max_length=20)
    ip_len = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return self.frame_number
        

