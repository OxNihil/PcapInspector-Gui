from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import PcapInfo

import json

from .core.generate_csv import load_pcap_to_model
from .core.filtering import load_filters_to_model
from .forms import FilterForm

# Auxiliar

def load_pcap(filename):
    # Borramos los datos de la tabla resultados
    PcapInfo.objects.all().delete()
    # generamos y cargamos csv al modelo
    load_pcap_to_model(filename)
    # Visualizamos los datos
    all_objects = PcapInfo.objects.all()
    context = {'uploaded_file_url': filename, 'all_packets': all_objects}
    return context


# Create your views here.
def index(request):
    form = FilterForm()
    # Datos captura
    pcap_data = PcapInfo.objects.all()
    context = {'all_packets': pcap_data, 'form': form}
    return render(request, 'index.html', context)


def upload(request):
    if request.method == 'POST' and request.FILES['pcap']:
        pcap_file = request.FILES['pcap']
        fs = FileSystemStorage()
        filename = fs.save(pcap_file.name, pcap_file)
        uploaded_file_url = fs.url(filename)
        context = load_pcap(uploaded_file_url)
        return render(request, 'upload.html', context)
    return render(request, 'upload.html')
