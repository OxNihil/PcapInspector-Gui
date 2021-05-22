import pandas as pd
import array
from django.shortcuts import render
from django.http import HttpResponse
from maps.dataCreation import lecturaDeDatos
from maps.dataCreation import Coordinadas

#from maps.models import Product,Review

# Create your views here.

#def index(request):
#	return HttpResponse("Hola mundo")

def index(request):
	dataIp = lecturaDeDatos.carga()
	dataGeo = pd.DataFrame() #json que devolve a utilización da API para geolocalizar ips
	network = []
	lat = []
	lon =[]

	a = 0
	while (a < len(dataIp)):
		dataGeo = dataGeo.append(Coordinadas.ipgeo(dataIp['network'][a]), ignore_index=True)
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

	print(lon)


	context = {'network': network,
			   'lat': lat,
			   'lon': lon,
			   'aux': 'aux'}

	#print(context)

	return render(request, '/home/marcos/Documents/pi-AnalisisPaqueteria-Iago-Marcos-Daniel/probas/myciao/maps/probaMaps.html', context)
