from django.shortcuts import render
from django.http import HttpResponse

#from maps.models import Product,Review

# Create your views here.

#def index(request):
#	return HttpResponse("Hola mundo")

def index(request):
	return render(request, '/home/marcos/Documents/myciao/maps/probaMaps.html')