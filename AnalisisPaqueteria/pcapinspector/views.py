from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import PcapInfo
from django.urls import reverse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .core.generate_csv import load_pcap_to_model
from .core.filtering import load_filters_to_model, analyze_dataframe
from .forms import FilterForm, LoginForm, SignupForm
from django_pandas.io import read_frame
import os.path
from django.conf import settings
from os import listdir, path
from os.path import isfile, join


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


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            f = UserCreationForm()
    form = SignupForm()
    return render(request, 'register.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index.html')
    form = LoginForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(request.GET['next'])

def list_pcaps():      
    context = {
        'list_pcaps':[],
        'path_pcaps':[]
    }
    # List of files in your MEDIA_ROOT
    media_path = settings.MEDIA_ROOT
    myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
    context['list_pcaps'] = myfiles
    for f in myfiles:
        context['path_pcaps'].append(settings.MEDIA_ROOT + "/" + f)

    return context


# Create your views here.
def index(request):
    login_error = ""

    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            login_error = "Se ha producido un error de login"

    form = FilterForm()
    # Datos captura
    pcap_data = PcapInfo.objects.all()
    login_form = LoginForm()
    signup_form = SignupForm()

    if request.user.is_authenticated:
        context = {'all_packets': pcap_data, 'form': form, 'login_form': login_form, 'signup_form ': signup_form,
                   'login_error': login_error}
    else:
        context = {'login_form': login_form, 'signup_form': signup_form, 'login_error': login_error}

    return render(request, 'index.html', context)


@login_required(login_url='/login')
def upload(request):
    login_error = ""

    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            login_error = "Se ha producido un error de login"

    login_form = LoginForm()
    signup_form = SignupForm()

    if request.method == 'POST' and request.FILES['pcap']:
        pcap_file = request.FILES['pcap']
        fs = FileSystemStorage()
        filename = fs.save(pcap_file.name, pcap_file)
        uploaded_file_url = fs.url(filename)
        context = load_pcap(uploaded_file_url)
        if request.user.is_authenticated:
            return render(request, 'upload.html', context.update(
                {'login_form': login_form, 'signup_form ': signup_form, 'login_error': login_error}))

    return render(request, 'upload.html',
                  {'login_form': login_form, 'signup_form ': signup_form, 'login_error': login_error})


@login_required(login_url='/login')
def stats(request):
    pcap_data = PcapInfo.objects.all()
    df = read_frame(pcap_data)
    # x = [x.protocol for x in pcap_data]
    chart_prots = analyze_dataframe(df).stats('protocol', 'Listado de protocolos', 'protocols')
    chart_ip_src = analyze_dataframe(df).stats('ip_src', 'Direcciones IPs de origen', 'IPs')
    chart_ip_dst = analyze_dataframe(df).stats('ip_dst', 'Direcciones IPs de destino', 'IPs')

    return render(request, 'stats.html', {'chart1': chart_prots, 'chart2': chart_ip_src, 'chart3': chart_ip_dst})

@login_required(login_url='/login')
def graph(request):
	pcap_data = PcapInfo.objects.all()
	df = read_frame(pcap_data)
	grafo = analyze_dataframe(df).show_graph()
	return render(request, 'graph.html', {'chart1': grafo })
	
@login_required(login_url='/login')
def pcaps(request):
    context = list_pcaps()
    print(context)
    return render(request, 'pcaps.html', context)
