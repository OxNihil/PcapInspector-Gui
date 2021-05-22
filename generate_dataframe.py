import os
import pandas as pd


def generate_dataframe(pcap_file):
    f_in = pcap_file
    f_out = "tmp.csv"
    tshark_template = 'tshark -r {} -T fields  -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport  ' \
                      '-e udp.srcport -e udp.dstport -e ip.ttl -e _ws.col.Protocol -e ip.len -E header=y -E separator=, -E quote=d -E occurrence=f > {}'
    tshark_command = tshark_template.format(f_in, f_out)
    os.system(tshark_command)
    df = pd.read_csv("tmp.csv")

    df.columns = df.columns.str.replace('.*srcport', 'port.src')
    df.columns = df.columns.str.replace('.*dstport', 'port.dst')
    s = df.stack()
    df = s.unstack()
    return df