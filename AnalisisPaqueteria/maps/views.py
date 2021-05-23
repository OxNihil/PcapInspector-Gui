import pandas as pd
from django.shortcuts import render
import sqlalchemy as sa
import pandas.io.sql as sql
import requests

#from maps.models import Product,Review

# Create your views here.

def carga():
    engine=sa.create_engine("sqlite:////tmp/db.sqlite")
    meta = sa.MetaData()
    tb = sa.Table( "IPs", meta, autoload_with=engine )

    db = pd.io.sql.SQLDatabase( engine, meta=meta )

    df = db.read_table("IPs")

    data = df.head(100)


    data = data['network']

    arrayDatos = data.to_numpy()



    for x in range(10):
        head, sep, tail = arrayDatos[x].partition('/')
        arrayDatos[x] = head


    dataF = pd.DataFrame(arrayDatos, columns=['network'])

    return dataF

def ipgeo(ip):

    url1 = "https://sys.airtel.lv/ip2country/" + ip + "/?full=true" #por ahora iremos usando esta

    #url1 = "http://api.ipstack.com/" + ip + "?access_key=fa3ea559085abe8f4a3eebbebd35695a"

    r = requests.get(url1)
    data = r.json()

    dataframe = {'network': ip, 'lat': data['lat'], 'lon': data['lon']}


    return dataframe


def index(request):
	dataIp = carga()
	dataGeo = pd.DataFrame()
	network = []
	lat = []
	lon =[]

	a = 0
	while (a < len(dataIp)):
		dataGeo = dataGeo.append(ipgeo(dataIp['network'][a]), ignore_index=True)
		a = a + 1


	b = 0
	while (b < len(dataIp)):
		network.append(str(dataGeo['network'][b]))
		b = b+1

	c = 0
	while (c < len(dataIp)):
		lat.append(str(dataGeo['lat'][c]))
		c = c + 1

	d = 0
	while (d < len(dataIp)):
		lon.append(str(dataGeo['lon'][d]))
		d = d + 1



	context = {'network': network, 'lat': lat, 'lon': lon}


	return render(request, 'probaMaps.html', context)
