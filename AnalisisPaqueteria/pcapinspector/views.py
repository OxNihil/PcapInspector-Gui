from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import PcapInfo, PacketInfo
from django.urls import reverse
import json
import requests
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .core.generate_csv import load_pcap_to_model
from .core.filtering import analyze_dataframe
from .core.network import net, analyze_scapy, data_analyze
from .forms import LoginForm, SignupForm
from django_pandas.io import read_frame
import os.path
from django.conf import settings
from os import listdir, path
from os.path import isfile, join, isdir


# Auxiliar
def load_scapy(requser):
    pd = PcapInfo.objects.filter(user=requser).first()
    if not pd:
        data = data_analyze()
        return data
    else:
        pcap = pd.pcap_url
        pcap_url = settings.BASE_DIR + pcap
        data = analyze_scapy(pcap_url).fast_scan()
        return data


def load_pcap(url, requser, filename):
    print(settings.BLACKLIST, filename)
    if filename in settings.BLACKLIST:
        return
    try:
        # Borramos las filas asociadas a la captura del user
        PcapInfo.objects.filter(user=requser).delete()
        # generamos y cargamos csv al modelo
        load_pcap_to_model(url, requser, filename)
        # Visualizamos los datos
        all_objects = PacketInfo.objects.filter(pcap__user=requser)
        context = {'uploaded_file_url': filename, 'all_packets': all_objects}
        return context
    except:
        return {}


@login_required(login_url='/login')
def report(request):
    requser = request.user
    data = load_scapy(requser)
    print("gateway:" + str(data.gateway))
    print("vlans:" + str(data.vlans))
    print("netbios: " + str(data.netbios))
    print("servers: " + str(data.servers))
    print("rootbridge:" + str(data.root_bridge))
    print("useragent: " + str(data.user_agents))
    print("dns_q: " + str(data.dnsqd))
    print("dns_an: " + str(data.dnsan))
    print("alerts: " + str(data.alerts))
    context = {'netdata': data}
    return render(request, 'report.html', context)


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


# necesito pasarlle o usuario
def list_pcaps(user):
    context = {
        'list_pcaps_example': [],
        'path_pcaps_example': [],
        'list_pcaps_user': [],
        'path_pcaps_user': [],

    }
    # List of files in your MEDIA_ROOT/example
    media_path = settings.MEDIA_ROOT + '/example'
    myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
    context['list_pcaps_example'] = myfiles
    for f in myfiles:
        context['path_pcaps_example'].append(settings.MEDIA_ROOT + "/example" + f)

    # List of files in your MEDIA_ROOT/user
    if user in listdir(settings.MEDIA_ROOT):
        media_path = settings.MEDIA_ROOT + '/' + user
        myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
        context['list_pcaps_user'] = myfiles
        for f in myfiles:
            context['path_pcaps_user'].append(settings.MEDIA_ROOT + "/" + user + '/' + f)

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

    login_form = LoginForm()
    signup_form = SignupForm()
    # Datos captura
    if request.user.is_authenticated:
        requser = request.user
        pcap_data = PacketInfo.objects.filter(pcap__user=requser)
        df = read_frame(pcap_data)
        ipsrc = analyze_dataframe(df).get_endpoints_ip()
        ipdst = analyze_dataframe(df).get_endpoints_ip_dst()
        protos = analyze_dataframe(df).get_endpoints_proto()
        macsrc = analyze_dataframe(df).get_endpoints_mac()
        macdst = analyze_dataframe(df).get_endpoints_mac_dst()
        portsrc = analyze_dataframe(df).get_endpoints_port()
        portdst = analyze_dataframe(df).get_endpoints_port_dst()
        context = {'all_packets': pcap_data, 'login_form': login_form, 'signup_form ': signup_form,
                   'login_error': login_error, 'ipsrc': ipsrc, 'ipdst': ipdst, 'protos': protos, 'portsrc': portsrc,
                   'portdst': portdst, 'macsrc': macsrc, 'macdst': macdst}
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
    if request.method == 'POST' and "pcap" not in request.FILES:
    	return render(request, 'nopcap.html')
    if request.method == 'POST' and (request.FILES['pcap'] and request.user.is_authenticated):
        media_path = settings.MEDIA_ROOT
        dir_exist = False
        for f in listdir(media_path):
            something = join(media_path, f)
            if isdir(something) and (str(f) == str(request.user)):
                dir_exist = True
                break
        if dir_exist == False:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, str(request.user)))
        pcap_file = request.FILES['pcap']
        if pcap_file.size > settings.MAX_UPLOAD_SIZE:
            context = {"maxsize": settings.MAX_UPLOAD_SIZE}
            return render(request, 'bigfile.html', context)
        print(pcap_file.size)
        pcap_file_split = str(pcap_file).split('.')
        if (pcap_file_split[1] == 'pcap') or (pcap_file_split[1] == 'pcapng') or (pcap_file_split[1] == 'cap'):
            requser = request.user
            user_path = media_path + '/' + str(requser)
            pcap_file.name = pcap_file.name.translate({ord(c): "_" for c in " !@#$%^&*()[]{};:,/<>?\|`~-=-+"})
            fs = FileSystemStorage(location=user_path, base_url=settings.MEDIA_URL + str(requser))
            filename = fs.save(pcap_file.name, pcap_file)
            uploaded_file_url = fs.url(filename)
            # print("Proba " + uploaded_file_url)
            load_pcap(uploaded_file_url, requser, filename)
            return redirect('index')
        else:
            return render(request, 'nopcap.html')

    return render(request, 'upload.html',
                  {'login_form': login_form, 'signup_form ': signup_form, 'login_error': login_error})


@login_required(login_url='/login')
def stats(request):
    requser = request.user
    pcap_data = PacketInfo.objects.filter(pcap__user=requser)
    if not pcap_data:
        return render(request, 'nopcap.html')
    df = read_frame(pcap_data)

    try:
        chart_protocols = analyze_dataframe(df).hist()
    except AttributeError:
        chart_protocols = ''
    chart_l_ip_src = analyze_dataframe(df).lollypop('ip_src', 'Source IP Address',
                                                    'Occurrences')
    chart_l_ip_dst = analyze_dataframe(df).lollypop('ip_dst', 'Destination IP Address',
                                                    'Occurrences')
    chart_p_src_port = analyze_dataframe(df).pie_chart('src_port', 'Most used source ports', 'Ports')
    chart_p_dst_port = analyze_dataframe(df).pie_chart('dst_port', 'Most used destination ports', 'Ports')
    if chart_protocols == '':
        return render(request, 'stats.html',
                      {'chart1': chart_l_ip_src, 'chart2': chart_l_ip_dst,
                       'chart3': chart_p_src_port,
                       'chart4': chart_p_dst_port})
    return render(request, 'stats.html',
                  {'chart0': chart_protocols, 'chart1': chart_l_ip_src, 'chart2': chart_l_ip_dst,
                   'chart3': chart_p_src_port,
                   'chart4': chart_p_dst_port})


@login_required(login_url='/login')
def ipinfo(request):
    requser = request.user
    pcap_data = PacketInfo.objects.filter(pcap__user=requser)
    df = read_frame(pcap_data)
    ABUSEIPDB_KEY = 'YOURAPIKEY'
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'
    ip_list = analyze_dataframe(df).get_endpoints_ip()

    headers = {
        'Accept': 'application/json',
        'Key': ABUSEIPDB_KEY
    }

    public_ips = []
    for ip in ip_list:
        if not net().is_local_net(ip):
            public_ips.append(ip)

    list_of_dicts = []
    for ip in public_ips:
        querystring = {'ipAddress': ip}
        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        if response.status_code == 200:
            # Formatted output
            decodedResponse = json.loads(response.text)
            abuse_score = decodedResponse['data']['abuseConfidenceScore']
            domain = decodedResponse['data']['domain']
            try:
                hostname = decodedResponse['data']['hostnames'][0]
            except IndexError:
                hostname = ''
            isp = decodedResponse['data']['isp']
            usage = decodedResponse['data']['usageType']

            dict = {"ip": ip, "domain": domain, "hostname": hostname, "isp": isp, "usage": usage, "abusescore": abuse_score}
            dict_copy = dict.copy()
            list_of_dicts.append(dict_copy)

    return render(request, 'ipinfo.html', {'api_info': list_of_dicts})


@login_required(login_url='/login')
def graph(request):
    if request.user.is_authenticated:
        requser = request.user
    pcap_data = PacketInfo.objects.filter(pcap__user=requser)
    df = read_frame(pcap_data)
    grafo = analyze_dataframe(df).show_graph()
    return render(request, 'graph.html', {'chart1': grafo})


@login_required(login_url='/login')
def pcaps(request):
    context = list_pcaps(str(request.user))
    return render(request, 'pcaps.html', context)


@login_required(login_url='/login')
def select_pcap(request, filename):
    # necesito saber de que carpeta teño que coller as cousas
    requser = request.user
    # context = load_pcap('/media/' + filename, requser)
    # solución bruta
    for f in listdir(settings.MEDIA_ROOT + '/example'):
        if f == filename:
            context = load_pcap('/media/example/' + filename, requser, filename)
            return index(request)
    context = load_pcap('/media/' + str(requser) + '/' + filename, requser, filename)
    # return render(request, 'pcaps.html', context)
    return index(request)
