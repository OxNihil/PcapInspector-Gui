import pandas as pd
import numpy as np
import os
from .generate_csv import dataframe_to_model,model_to_dataframe
from pcapinspector.models import *
 

class filters():
	def __init__(self,opts):
		self.ports = opts.portFilter
		self.protocols = opts.protoFilter
	def protocol(self,row):
		if (self.protocols != ""):
			protocols_f = self.protocols.split(",")
			protocols_f = [x.upper() for x in protocols_f]
			proto = row["protocol"]
			if proto not in protocols_f:
				return True
			return False
		else:
			return False
	
	def port(self,row):
		if (self.ports != ""):
			ports_src = row["src_port"]
			ports_dst = row["dst_port"]
			if (np.isnan(ports_src) or np.isnan(ports_dst)):
				return False
			ports_f = self.ports.split(",")
			ports_f = [int(x) for x in ports_f]
			if (ports_f.count(ports_src) > 0 or ports_f.count(ports_dst) > 0):
				return True
			return False
		else:
			return False
			
class analyze_dataframe():
	def __init__(self,df):
	    self.df = df
	def get_endpoints_ip(self):
	    all_ips = df["ip_src"].dropna().unique()
	    all_ips = list(dict.fromkeys(all_ips))
	    return all_ips
	def get_endpoints_mac(self):
	    all_mac = df["eth.src"].dropna().unique()
	    all_mac = list(dict.fromkeys(all_mac))
	    return all_macs
	def filter_dataframe(self,opts):
	    filtro = filters(opts)
	    #Iteramos sobre las filas del dataframe
	    #Eliminamos las que esten para filtrar
	    for index,row in self.df.iterrows():
	        if(filtro.port(row)):
	            self.df = self.df.drop(index)
	            continue
	        if (filtro.protocol(row)):
	            self.df = self.df.drop(index)
	            continue
	    return self.df

#Registro	
class opts():
   def __init__(self,port,proto):
       self.portFilter = port
       self.protoFilter = proto

def load_filters_to_model(protocol,port):
    opt = opts(protocol,port)
    df = model_to_dataframe(pcap_result)
    analyze_df = analyze_dataframe(df)
    df = analyze_df.filter_dataframe(opt)
    modelo = dataframe_to_model(df,pcap_result)


