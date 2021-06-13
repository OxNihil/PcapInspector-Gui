from maps.views import ipgeo
from django.test import TestCase
from django.test import Client
from django.contrib.auth import models

class ViewsTestCase(TestCase):

    def test_geolocalizacion_ip_public(self):
        dataframe = ipgeo("142.250.182.68")
        self.assertEquals(dataframe['network'], "142.250.182.68")
        self.assertEquals(dataframe['lat'], "38.01")
        self.assertEquals(dataframe['lon'], "-122.12")
    

    def test_geolocalizacion_ip_private(self):
        dataframe = ipgeo("10.215.173.1")
        self.assertEquals(dataframe['network'], "10.215.173.1")
        self.assertEquals(dataframe['lat'], "0.00")
        self.assertEquals(dataframe['lon'], "0.00")