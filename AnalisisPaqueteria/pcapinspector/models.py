from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class PcapInfo(models.Model):
	pcap_id = models.AutoField(default=None,primary_key=True) 
	pcap_name = models.CharField(max_length=120)
	pcap_url = models.CharField(max_length=200,null=False,blank=False)
	user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
	def __str__(self):
		return "%s %s" % (self.pcap_name,self.user)
	class Meta:
		unique_together = (('pcap_name','user'),)

# Create your models here.
class PacketInfo(models.Model):
    packet_id = models.AutoField(primary_key=True) 
    frame_number = models.IntegerField(null=True,blank=True)
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
    pcap = models.ForeignKey(PcapInfo,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.frame_number
    def __str__(self):
    	return "%s %s" % (self.frame_number,self.user)
    class Meta:
    	unique_together = (('frame_number','pcap'),)
        
