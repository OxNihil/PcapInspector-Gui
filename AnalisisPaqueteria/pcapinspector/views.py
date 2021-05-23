from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from pcapinspector.models import pcap_result

import json

from .core.generate_csv import load_pcap_to_model
from .core.filtering import load_filters_to_model
from .forms import FilterForm

#Auxiliar
   
def load_pcap(filename):
	#Borramos los datos de la tabla resultados
	pcap_result.objects.all().delete()
	#generamos y cargamos csv al modelo
	load_pcap_to_model(filename)
	#Visualizamos los datos
	all_objects = pcap_result.objects.all()
	context =  {'uploaded_file_url': filename,'all_packets': all_objects }
	return context

# Create your views here.
def index(request):
    #si el formulario es valido filtramos
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            port = form.cleaned_data.get('protocol')
            protocol = form.cleaned_data.get('port')
            load_filters_to_model(protocol,port)
    else:
        form = FilterForm()
    #Datos captura
    pcap_data = pcap_result.objects.all()
    context =  {'all_packets': pcap_data, 'form': form } 
    return render(request,'index.html',context)
   
def upload(request):
    if request.method == 'POST' and request.FILES['pcap']:
    	pcap_file = request.FILES['pcap']
    	fs = FileSystemStorage()
    	filename = fs.save(pcap_file.name, pcap_file)
    	uploaded_file_url = fs.url(filename)
    	context = load_pcap(uploaded_file_url)
    	return render(request,'packets.html',context)
    return render(request, 'upload.html')

