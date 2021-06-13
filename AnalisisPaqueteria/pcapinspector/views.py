from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import PcapInfo
from django.urls import reverse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .core.generate_csv import load_pcap_to_model
from .core.filtering import load_filters_to_model
from .forms import FilterForm, LoginForm, SignupForm


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


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(request.GET['next'])


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
        context = {'all_packets': pcap_data, 'form': form, 'login_form': login_form, 'signup_form ': signup_form ,
                   'login_error': login_error}
    else:
        context = {'login_form': login_form, 'signup_form': signup_form, 'login_error': login_error}

    return render(request, 'index.html', context)


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
