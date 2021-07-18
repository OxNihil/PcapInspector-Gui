import pandas as pd
from django.shortcuts import render
import sqlalchemy as sa
import pandas.io.sql as sql
import requests
import datapackage
from pcapinspector.models import PacketInfo
from django.contrib.auth.decorators import login_required
from pcapinspector.core.network import *


def load(requser):
    ip_result = []
    ip_return = []
    ip_info = PacketInfo.objects.filter(pcap__user=requser)

    if not ip_info :
        return None

    for ip in ip_info:
        ip_result.append(ip.ip_src)
        ip_result.append(ip.ip_dst)

    ip_list = pd.DataFrame({'network': ip_result})
    ip_list = ip_list['network'].dropna().unique()

    for ip in ip_list:
        if ip == '':
            continue
        public = ip.split('.')
        num1 = int(public[0])
        num2 = int(public[1])
        num3 = int(public[2])
        num4 = int(public[3])

        if (num1 >= 224 and num1 <= 239):
            continue
        if num1 == 192 and num2 == 168 and num4 == 255:
            continue
        if num1 == 255 and num2 == 255 and num3 == 255 and num4 == 255:
            continue
        if num1 == 127:
            continue
        if (num1 == 192 and num2 == 168):
            continue
        if num1 == 10:
            continue
        if num1 == 172 and (int(num2) > 15 and int(num2) < 32):
            continue
        ip_return.append(ip)

    ip_list = pd.DataFrame({'network': ip_return})

    return ip_list


def ipgeo(ip):
    url1 = "https://sys.airtel.lv/ip2country/" + ip + "/?full=true"  # por ahora iremos usando esta

    r = requests.get(url1)
    data = r.json()
    dataframe = {'network': ip, 'lat': data['lat'], 'lon': data['lon']}
    return dataframe


@login_required(login_url='/login')
def index(request):
    requser = request.user
    dataIp = load(requser)

    if type(dataIp) == type(None):
        return render(request, 'nopcap.html')  # Hai que comprobar na vista que non se recive nada nos templates

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
