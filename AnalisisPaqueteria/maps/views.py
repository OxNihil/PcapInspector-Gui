import pandas as pd
from django.shortcuts import render
import sqlalchemy as sa
import pandas.io.sql as sql
import requests
import datapackage
from pcapinspector.models import PcapInfo


def load():
	ip_result = []
	ip_return = []
	ip_info = PcapInfo.objects.all()

	for ip in ip_info:
		ip_result.append(ip.ip_src)
		ip_result.append(ip.ip_dst)

	ip_list = pd.DataFrame({'network': ip_result})
	ip_list = ip_list['network'].dropna().unique()

	print(ip_list)


	for ip in ip_list :
		public = ip.split('.')
		num = int(public[0])
		if ((num >= 1 & num <=126) | (num >= 128 & num <=191) | (num >= 192 & num <=223)) :
			ip_return.append(ip)

	ip_list = pd.DataFrame({'network': ip_return})

	return ip_list


def ipgeo(ip):

    url1 = "https://sys.airtel.lv/ip2country/" + ip + "/?full=true" #por ahora iremos usando esta

    r = requests.get(url1)
    data = r.json()

    dataframe = {'network': ip, 'lat': data['lat'], 'lon': data['lon']}


    return dataframe


def index(request):

	dataIp = load()

	if dataIp.empty:
		return render(request, 'nopcap.html') #Hai que comprobar na vista que non se recive nada nos templates

	dataGeo = pd.DataFrame()
	network = []
	lat = []
	lon = []

	a = 0
	while (a < len(dataIp)):
		dataGeo = dataGeo.append(ipgeo(dataIp['network'][a]), ignore_index=True)
		a = a + 1

	b = 0
	while (b < len(dataIp)):
		network.append(str(dataGeo['network'][b]))
		lat.append(str(dataGeo['lat'][b]))
		lon.append(str(dataGeo['lon'][b]))
		b = b + 1


	context = {'network': network, 'lat': lat, 'lon': lon}


	return render(request, 'maps.html', context)
