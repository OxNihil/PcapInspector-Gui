import unittest
from django.test import TestCase
from pcapinspector.models import PcapInfo, PacketInfo
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import AnonymousUser, User
#from django.contrib.auth.models.AnonymousUser import delete


class ModelsTestCase(TestCase):

#    class PcapInfo(models.Model):
#    pcap_id = models.AutoField(default=None,primary_key=True) 
#    pcap_name = models.CharField(max_length=120)
#    pcap_url = models.CharField(max_length=200,null=False,blank=False)
#    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
#    def __str__(self):
#        return "%s %s" % (self.pcap_name,self.user)
#    class Meta:
#        unique_together = (('pcap_name','user'),)


#class PacketInfo(models.Model):
#    packet_id = models.AutoField(primary_key=True) 
#    frame_number = models.IntegerField(null=True,blank=True)
#    frame_time = models.CharField(max_length=50)
#    eth_src = models.CharField(max_length=20,null=True,blank=True)
#    eth_dst = models.CharField(max_length=20,null=True,blank=True)
#    ip_src = models.CharField(max_length=16,null=True, blank=True)
#    ip_dst = models.CharField(max_length=16,null=True,blank=True)
#    src_port = models.IntegerField(null=True, blank=True)
#    dst_port = models.IntegerField(null=True, blank=True)
#    ttl = models.IntegerField(null=True,blank=True)
#    protocol = models.CharField(max_length=20)
#    ip_len = models.IntegerField(null=True,blank=True)
#    pcap = models.ForeignKey(PcapInfo,on_delete=models.CASCADE)
#    def __unicode__(self):
#        return self.frame_number
#    def __str__(self):
#        return "%s %s" % (self.frame_number,self.pcap)
#    class Meta:
#        unique_together = (('frame_number','pcap'),)

    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        pcap = PcapInfo.objects.create(pcap_name = "pcap.pcap", pcap_url = "/home/media", user = self.user)
        PacketInfo.objects.create(frame_number=1, frame_time="Apr 25, 2021 22:55:03.226624000 CEST", eth_src=None, eth_dst=None, ip_src="10.215.173.1", ip_dst="10.215.173.2", src_port=21039, dst_port=53, ttl=64, protocol="DNS", ip_len=60, pcap=pcap)
        PacketInfo.objects.create(frame_number=2, frame_time="Apr 25, 2021 23:55:03.226624000 CEST", eth_src=None, eth_dst=None, ip_src="10.215.173.2", ip_dst="10.215.173.3", src_port=21039, dst_port=53, ttl=64, protocol="DNS", ip_len=60, pcap=pcap)


    def test_products(self):
        # Recuperamos los dos productos y comprobamos sus campos
        pi = PcapInfo.objects.get(pcap_name = 'pcap.pcap')
        self.assertEquals(pi.pcap_name, 'pcap.pcap')
        self.assertEquals(pi.pcap_url, '/home/media')
        self.assertEquals(pi.user, self.user)



        p = PacketInfo.objects.get(frame_number=1)
        self.assertEquals(p.frame_number, 1)
        self.assertEquals(p.frame_time, "Apr 25, 2021 22:55:03.226624000 CEST")
        self.assertEquals(p.eth_src, None)
        self.assertEquals(p.eth_dst, None)
        self.assertEquals(p.ip_src, "10.215.173.1")
        self.assertEquals(p.ip_dst, "10.215.173.2")
        self.assertEquals(p.src_port, 21039)
        self.assertEquals(p.dst_port, 53)
        self.assertEquals(p.ttl, 64)
        self.assertEquals(p.protocol, "DNS")
        self.assertEquals(p.ip_len, 60)

        p = PacketInfo.objects.get(frame_number=2)
        self.assertEquals(p.frame_number, 2)
        self.assertEquals(p.frame_time, "Apr 25, 2021 23:55:03.226624000 CEST")
        self.assertEquals(p.eth_src, None)
        self.assertEquals(p.eth_dst, None)
        self.assertEquals(p.ip_src, "10.215.173.2")
        self.assertEquals(p.ip_dst, "10.215.173.3")
        self.assertEquals(p.src_port, 21039)
        self.assertEquals(p.dst_port, 53)
        self.assertEquals(p.ttl, 64)
        self.assertEquals(p.protocol, "DNS")
        self.assertEquals(p.ip_len, 60)

    @unittest.expectedFailure
    def test_product(self):
        # Test que debe fallar porque no hay tantas reviews
        r = PcapInfo.objects.get(id=2434234)

    def deletBD(self):
        PcapInfo.objects.filter(user=self.user).delete()