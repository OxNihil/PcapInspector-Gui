from maps.views import ipgeo
from django.test import TestCase
from django.test import Client
from django.contrib.auth import models
import requests
import json


#@login_required(login_url='/login')
#def ipinfo(request):
#    requser = request.user
#    pcap_data = PacketInfo.objects.filter(pcap__user=requser)
#    df = read_frame(pcap_data)
#    ABUSEIPDB_KEY = 'YOURAPIKEY'
#    # Defining the api-endpoint
#    url = 'https://api.abuseipdb.com/api/v2/check'
#    ip_list = analyze_dataframe(df).get_endpoints_ip()

#    headers = {
#        'Accept': 'application/json',
#        'Key': ABUSEIPDB_KEY
#    }

#    public_ips = []
#    for ip in ip_list:
#        if not net().is_local_net(ip):
#            public_ips.append(ip)

#    list_of_dicts = []
##    for ip in public_ips:
#        querystring = {'ipAddress': ip}
#        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
#        if response.status_code == 200:
#            # Formatted output
#            decodedResponse = json.loads(response.text)
#            abuse_score = decodedResponse['data']['abuseConfidenceScore']
#            domain = decodedResponse['data']['domain']
#            try:
#                hostname = decodedResponse['data']['hostnames'][0]
#            except IndexError:
#                hostname = ''
#            usage = decodedResponse['data']['usageType']

#            dict = {"ip": ip, "domain": domain, "hostname": hostname, "usage": usage, "abusescore": abuse_score}
#            dict_copy = dict.copy()
#            list_of_dicts.append(dict_copy)

#    return render(request, 'ipinfo.html', {'api_info': list_of_dicts})



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

    def test_pcapinfo(self):
        querystring = {'ipAddress': '142.250.182.68'}
        ABUSEIPDB_KEY = 'YOURAPIKEY'
        url = 'https://api.abuseipdb.com/api/v2/check'
        headers = {
            'Accept': 'application/json',
            'Key': ABUSEIPDB_KEY
        }
        response = requests.request(method='GET', url=url, headers=headers, params=querystring)

        decodedResponse = json.loads(response.text)

        self.assertEquals(decodedResponse['data']['ipVersion'], 4)
        self.assertEquals(decodedResponse['data']['isPublic'], True)
        self.assertEquals(decodedResponse['data']['isWhitelisted'], None)
        self.assertEquals(decodedResponse['data']['isp'], "Google LLC")
        self.assertEquals(decodedResponse['data']['lastReportedAt'], None)
        self.assertEquals(decodedResponse['data']['numDistinctUsers'], 0)
        self.assertEquals(decodedResponse['data']['totalReports'], 0)
        self.assertEquals(decodedResponse['data']['usageType'], "Data Center/Web Hosting/Transit")

