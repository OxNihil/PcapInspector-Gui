import pandas as pd
from django.shortcuts import render
import sqlalchemy as sa
import pandas.io.sql as sql
import requests
import datapackage




def saveData():
	data_url = 'https://datahub.io/core/geoip2-ipv4/datapackage.json'

	# to load Data Package into storage
	package = datapackage.Package(data_url)

	resources = package.resources
	for resource in resources:
		if resource.tabular:
			data = pd.read_csv(resource.descriptor['path'])

	engine = sa.create_engine( "sqlite:////tmp/db.sqlite" )
	db = pd.io.sql.SQLDatabase(engine)
	tb = pd.io.sql.SQLTable(name="IPs", pandas_sql_engine=db, frame=data)
	tb.create()
	tb.insert()

# Create your views here.

def load():
	engine = sa.create_engine("sqlite:////tmp/db.sqlite")
	meta = sa.MetaData()
	tb = sa.Table("IPs", meta, autoload_with=engine)

	db = pd.io.sql.SQLDatabase(engine, meta=meta)

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
	try:
		saveData()
		pass
	except Exception as e:
		print(e)
	dataIp = load()
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


	return render(request, 'probaMaps.html', context)
