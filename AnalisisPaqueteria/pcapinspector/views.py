from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from pcapinspector.models import pcap_result
import json

from .core import dataframe


# Create your views here.
def index(request):
    return render(request,'index.html')
    
def processed_pcap(filename):
	#Borramos los datos de la tabla resultados
	pcap_result.objects.all().delete()
	#Establecer opciones de filtrado
	df = dataframe.analyze_pcap(filename)
	#Añadimos datos
	json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
	for dic in json_list:
	     pcap_result.objects.get_or_create(**dic)
	#Visualizamos los datos
	all_objects = pcap_result.objects.all()
	print(all_objects)
	context =  {'uploaded_file_url': filename,'all_packets': all_objects}
	return context


def upload(request):
    if request.method == 'POST' and request.FILES['pcap']:
    	pcap_file = request.FILES['pcap']
    	fs = FileSystemStorage()
    	filename = fs.save(pcap_file.name, pcap_file)
    	uploaded_file_url = fs.url(filename)
    	context = processed_pcap(uploaded_file_url)
    	return render(request,'packets.html',context)
    return render(request, 'upload.html')

