import pandas as pd
import numpy as np
from scapy.all import *
import os
from django.conf import settings

def generate_dataframe(pcap_file):
    f_in = settings.BASE_DIR+pcap_file
    f_out = "tmp/tmp.csv"
    tshark_template = 'tshark -r {} -T fields  -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport  ' \
                      '-e udp.srcport -e udp.dstport -e ip.ttl -e _ws.col.Protocol -e ip.len -E header=y -E separator=, -E quote=d -E occurrence=f > {}'
    tshark_command = tshark_template.format(f_in, f_out)
    os.system(tshark_command)
    df = pd.read_csv("tmp/tmp.csv")
    df.columns = df.columns.str.replace('.*srcport', 'port.src')
    df.columns = df.columns.str.replace('.*dstport', 'port.dst')
    return df


class filters():
	def __init__(self,opts):
		self.ports = opts.portFilter
		self.protocols = opts.protoFilter
	def protocol(self,row):
		if (self.protocols != ""):
			protocols_f = self.protocols.split(",")
			protocols_f = [x.upper() for x in protocols_f]
			proto = row["_ws.col.Protocol"]
			if proto not in protocols_f:
				return True
			return False
		else:
			return False
	
	def port(self,row):
		if (self.ports != ""):
			ports_src = row["port.src"]
			ports_dst = row["port.dst"]
			if (np.isnan(ports_src) or np.isnan(ports_dst)):
				return False
			ports_f = self.ports.split(",")
			ports_f = [int(x) for x in ports_f]
			ports_src = int(row["_ws.col.SrcPort"])
			ports_dst = int(row["_ws.col.DstPort"])
			if (ports_f.count(ports_src) > 0 or ports_f.count(ports_dst) > 0):
				return True
			return False
		else:
			return False
			
def analyze_pcap(pcap_file):
	#Generamos csv
	df = generate_dataframe(pcap_file)
	filtro = filters(opts)
	#Iteramos sobre las filas del dataframe
	for index,row in df.iterrows():
		if(filtro.port(row)):
			df = df.drop(index)
			continue
		if (filtro.protocol(row)):
			df = df.drop(index)
			continue
	#Cambiamos el formato del tiempo para que sea compatible
	df['frame.time'] = df['frame.time'].astype(np.float).astype("Int32")
	#Renombramos dataframe para que se adapte al modelo
	cols =  {'frame.number':'frame_number', 'frame.time':'frame_time','eth.src':'eth_src',
	'eth.dst':'eth_dst','ip.src':'ip_src','ip.dst':'ip_dst','ip.len':'ip_len','ip.ttl':'ttl',
	'port.dst':'dst_port','port.src':'src_port','_ws.col.Protocol':'protocol'}
	df = df.rename(columns = cols,inplace = False)
	#Convertimos tipos para poder serializarlo
	s = df.stack()
	df = s.unstack()
	return df

#Registro
class opts:
	portFilter = ""
	protoFilter = ""
	pcap_name = ""
