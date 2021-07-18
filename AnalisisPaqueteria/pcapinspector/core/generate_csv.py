import pandas as pd
import numpy as np
import os
import csv
import json
from django.conf import settings
from pcapinspector.models import PcapInfo, PacketInfo
from django_pandas.io import read_frame


def gen_csv(pcap_file):
    f_in = settings.BASE_DIR + pcap_file
    # print('Estes es el directorio base ' + settings.BASE_DIR + '\n')
    # print('Estes es el directorio f_in ' + f_in + '\n')
    f_out = settings.BASE_DIR + "/pcapinspector/tmp/tmp.csv"
    # f_out = "pcapinspector/tmp/tmp.csv"
    tshark_template = 'tshark -r {} -T fields  -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport  ' \
                      '-e udp.srcport -e udp.dstport -e ip.ttl -e _ws.col.Protocol -e ip.len -E header=y -E separator=, -E quote=d -E occurrence=f > {}'
    tshark_command = tshark_template.format(f_in, f_out)
    os.system(tshark_command)
    return f_out


# frame.number,frame.time,eth.src,eth.dst,ip.src,ip.dst,tcp.srcport,tcp.dstport,udp.srcport,udp.dstport,ip.ttl,_ws.col.Protocol,ip.len
def load_csv_to_model(path, fpcap):
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
                _, created = PacketInfo.objects.update_or_create(
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
                    ip_len=row[12],
                    pcap=fpcap
                )
            except Exception as e:
                continue


def load_pcap_info_model(pcap_file, requser, filename):
    PcapInfo.objects.filter(user=requser).delete()
    p = PcapInfo.objects.create(pcap_name=filename, pcap_url=pcap_file, user=requser)
    return p


def load_pcap_to_model(pcap_file, requser, filename):
    csv_path = gen_csv(pcap_file)
    df = csv_to_dataframe(csv_path)
    pcap = load_pcap_info_model(pcap_file, requser, filename)
    pandas_to_model(df, pcap)


def csv_to_dataframe(path):
    df = pd.read_csv(path)
    return df


def model_to_dataframe(modelo):
    data = modelo.objects.all()
    df = read_frame(data)
    return df


def parse_record(record):
    for r in record:
        try:
            if r == "eth.src" or r == "eth.dst" or r == "ip.src" or r == "ip.dst":
                if np.isnan(record[r]):
                    record[r] = ""
            else:
                if np.isnan(record[r]):
                    record[r] = np.nan_to_num(record[r])
        except:
            continue
    return record


def pandas_to_model(df, fpcap):
    df_records = df.to_dict('records')
    model_instances = []
    for record in df_records:
        record = parse_record(record)
        srcport = 0
        dstport = 0
        if record['tcp.srcport'] > 0:
            srcport = record['tcp.srcport']
        elif record['udp.srcport'] > 0:
            srcport = record['udp.srcport']
        if record['tcp.dstport'] > 0:
            dstport = record['tcp.dstport']
        elif record['udp.dstport'] > 0:
            dstport = record['udp.dstport']
        srcport = int(float(srcport))
        dstport = int(float(dstport))
        packet = PacketInfo(
            frame_number=record['frame.number'],
            frame_time=record['frame.time'],
            eth_src=record['eth.src'],
            eth_dst=record['eth.dst'],
            ip_src=record['ip.src'],
            ip_dst=record['ip.dst'],
            src_port=srcport,
            dst_port=dstport,
            ttl=record['ip.ttl'],
            protocol=record['_ws.col.Protocol'],
            ip_len=record['ip.len'],
            pcap=fpcap,
        )
        model_instances.append(packet)
    PacketInfo.objects.bulk_create(model_instances)
