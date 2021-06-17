import unittest
from django.test import TestCase
from pcapinspector.models import PcapInfo


class ModelsTestCase(TestCase):
    # Fixture: preparación de los datos a probar
    def setUp(self):
        PcapInfo.objects.create(frame_number=1, frame_time="Apr 25, 2021 22:55:03.226624000 CEST", eth_src=None, eth_dst=None, ip_src="10.215.173.1", ip_dst="10.215.173.2", src_port=21039, dst_port=53, ttl=64, protocol="DNS", ip_len=60)
        PcapInfo.objects.create(frame_number=2, frame_time="Apr 25, 2021 23:55:03.226624000 CEST", eth_src=None, eth_dst=None, ip_src="10.215.173.2", ip_dst="10.215.173.3", src_port=21039, dst_port=53, ttl=64, protocol="DNS", ip_len=60)

    def test_products(self):
        # Recuperamos los dos productos y comprobamos sus campos
        p = PcapInfo.objects.get(frame_number=1)
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

        p = PcapInfo.objects.get(frame_number=2)
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