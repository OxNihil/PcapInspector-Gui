import pandas as pd
import numpy as np
import os
import csv
import json
from django.conf import settings
from pcapinspector.models import PcapInfo
from django_pandas.io import read_frame


def gen_csv(pcap_file):
    f_in = settings.BASE_DIR + pcap_file
    f_out = "pcapinspector/tmp/tmp.csv"
    tshark_template = 'tshark -r {} -T fields  -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport  ' \
                      '-e udp.srcport -e udp.dstport -e ip.ttl -e _ws.col.Protocol -e ip.len -E header=y -E separator=, -E quote=d -E occurrence=f > {}'
    tshark_command = tshark_template.format(f_in, f_out)
    os.system(tshark_command)
    return f_out


# frame.number,frame.time,eth.src,eth.dst,ip.src,ip.dst,tcp.srcport,tcp.dstport,udp.srcport,udp.dstport,ip.ttl,_ws.col.Protocol,ip.len
def load_csv_to_model(path):
    with open(path) as f:
        reader = csv.reader(f)
        # Saltamos las cabeceras
        next(reader, None)
        for row in reader:
            try:
                srcport = ""
                dstport = ""
                if (row[6] != ""):
                    srcport = row[6]
                elif (row[8] != ""):
                    srcport = row[8]
                if (row[7] != ""):
                    dstport = row[7]
                elif (row[9] != ""):
                    dstport = row[9]
                _, created = PcapInfo.objects.get_or_create(
                    frame_number=row[0],
                    frame_time=row[1],
                    eth_src=row[2],
                    eth_dst=row[3],
                    ip_src=row[4],
                    ip_dst=row[5],
                    src_port=srcport,
                    dst_port=dstport,
                    ttl=row[10],
                    protocol=row[11],
                    ip_len=row[12]
                )
            except:
                continue


def load_pcap_to_model(pcap_file):
    csv_path = gen_csv(pcap_file)
    load_csv_to_model(csv_path)


def csv_to_dataframe(path):
    df = pd.read_csv(path)
    return df


def model_to_dataframe(modelo):
    data = modelo.objects.all()
    df = read_frame(data)
    return df


def dataframe_to_model(df, modelo):
    # Borramos datos previos
    modelo.objects.all().delete()
    s = df.stack()
    df = s.unstack()
    # Añadimos datos
    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
    for dic in json_list:
        modelo.objects.get_or_create(**dic)
    return modelo
