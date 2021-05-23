from django.db import models

# Create your models here.
class pcap_result(models.Model):
    frame_number=models.CharField(max_length=10,primary_key=True)
    frame_time=models.CharField(max_length=50)
    eth_src=models.CharField(max_length=20)
    eth_dst=models.CharField(max_length=20)
    ip_src=models.CharField(max_length=16)
    ip_dst=models.CharField(max_length=16)
    src_port=models.IntegerField(null=True,blank=True)
    dst_port=models.IntegerField(null=True,blank=True)
    ttl=models.IntegerField()
    protocol=models.CharField(max_length=20)
    ip_len=models.IntegerField()
    def __unicode__(self):
        return self.name
        
      

