import base64
import networkx as nx
import pandas as pd
import numpy as np
import os
from .generate_csv import dataframe_to_model, model_to_dataframe
from pcapinspector.models import PcapInfo
import matplotlib.pyplot as plt
from django.conf import settings
from io import StringIO, BytesIO


class filters():
    def __init__(self, opts):
        self.ports = opts.portFilter
        self.protocols = opts.protoFilter

    def protocol(self, row):
        if self.protocols != "":
            protocols_f = self.protocols.split(",")
            protocols_f = [x.upper() for x in protocols_f]
            proto = row["protocol"]
            if proto not in protocols_f:
                return True
            return False
        else:
            return False

    def port(self, row):
        if self.ports != "":
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
    def __init__(self, df):
        self.df = df

    def get_endpoints_ip(self):
        all_ips = self.df["ip_src"].dropna().unique()
        all_ips = list(dict.fromkeys(all_ips))
        return all_ips

    def get_endpoints_mac(self):
        all_mac = self.df["eth.src"].dropna().unique()
        all_mac = list(dict.fromkeys(all_mac))
        return all_mac

    def filter_dataframe(self, opts):
        filtro = filters(opts)
        # Iteramos sobre las filas del dataframe
        # Eliminamos las que esten para filtrar
        for index, row in self.df.iterrows():
            if (filtro.port(row)):
                self.df = self.df.drop(index)
                continue
            if (filtro.protocol(row)):
                self.df = self.df.drop(index)
                continue
        return self.df
    
    def create_graph(self):
	    G = nx.Graph()
	    all_ips = self.df["ip_src"].dropna().unique()
	    all_ips = list(dict.fromkeys(all_ips))
	    ips_grp = self.df.groupby(["ip_src","ip_dst"])
	    ips_protos = ips_grp["protocol"].unique()
	    ips_protos_dst = ips_grp["ip_dst"].unique()
	    for i in all_ips:
	    	#solo almacenamos nodos de ips locales
		    if(net().is_local_unicast(str(i))):
		        G.add_node(str(i))
		    else:
		    	continue
		    #Recorremos el dataframe y obtenemos el dst y protocolos
		    for j in range(len(ips_protos[i])):
		        proto_ip = ips_protos[i].iloc[j]
		        dst_ip = ips_protos_dst[i].iloc[j][0]	
		        #Comprobamos si la ip de destino es local
		        if (net().is_local_net(dst_ip)):
		        	if i != j:
		        		G.add_edge(i,str(dst_ip),proto=proto_ip)
		        #La ip de destino es externa
		        G.add_node("Internet") #WAN
		        G.add_edge(i,"Internet",proto=proto_ip) 
		        #De internet al nodo externo objetivo
		        tag = str(proto_ip) 
		        G.add_edge("Internet",str(dst_ip),proto=tag)
	    return G
    def show_graph(self):
        plt.figure(figsize=(12, 7))
        G = self.create_graph()
        pos = nx.spring_layout(G)
        nx.draw_networkx(G,pos)
        # labels
        labels = nx.get_edge_attributes(G, 'proto')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        #save graph
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        data = buf.getvalue()
        graph = base64.b64encode(data)
        graph = graph.decode('utf-8')
        buf.close()
        plt.close()
        return graph
       
    def func(self, pct, allvals):
        absolute = int(round(pct / 100. * np.sum(allvals)))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    def stats(self, column, title, legend):
        valor = 4  # numero de items que queremos mostrar en la leyenda de forma independiente
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        data = self.df[column].value_counts()
        protocols, values = data.index.tolist(), data.tolist()
        protocols_toprint, values_toprint = protocols[:valor], values[:valor]
        if len(values) > valor:
            #protocols_toprint.append("Others: " + str(protocols[valor:len(protocols)]))
            protocols_toprint.append("Others")

            values_toprint.append(np.sum(values[valor:len(values)]))

        wedges, texts, autotexts = ax.pie(values_toprint,
                                          autopct=lambda pct: analyze_dataframe(self.df).func(pct, values_toprint),
                                          textprops=dict(color="w"))
        ax.legend(wedges, protocols_toprint,
                  title=legend,
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title(title)
        # analyze_dataframe(df).stats('_ws.col.Protocol', "Listado de protocolos", "Protocolos")
        #plt.savefig(legend + ".png")
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        data = buffer.getvalue()
        graph = base64.b64encode(data)
        graph = graph.decode('utf-8')
        buffer.close()
        plt.close()
        return graph


class net():
	def return_ttl_so_name(self,ttl_number):
		if ttl_number >= 0 and ttl_number <= 64:
			return "Linux"
		elif ttl_number >= 65 and ttl_number <=128:
			return "Windows"
		else:	
			return "Uknown"	
			
	def is_multicast(self,ip):
		octetos = ip.split(".")
		if octetos[0] == "224" and octetos[1] == "0" and octetos[2] == "0":
			return True
		return False
		
	def is_broadcast(self,ip):
		octetos = ip.split(".")
		if octetos[0] == "192" and octetos[1] == "168" and octetos[3] == "255":
			return True
		elif octetos[0] == "255" and octetos[1] == "255" and octetos[2] == "255" and octetos[3] == "255":
			return True
		return False
		
	def is_local_unicast(self,ip):
		octetos = ip.split(".")
		if octetos[0] == "127":
			return True
		elif (octetos[0] =="192" and octetos[1] =="168"):
			return True
		elif octetos[0] == "10":
			return True
		elif octetos[0] == "172" and (int(octetos[1]) > 15 and int(octetos[1]) < 32):
			return True
		return False

	def is_local_net(self,ip):
		if (self.is_broadcast(ip) or self.is_multicast(ip) or self.is_local_unicast(ip)):
			return True
		return False

# Registro
class opts():
    def __init__(self, port, proto):
        self.portFilter = port
        self.protoFilter = proto


def load_filters_to_model(protocol, port):
    opt = opts(protocol, port)
    df = model_to_dataframe(PcapInfo)
    analyze_df = analyze_dataframe(df)
    df = analyze_df.filter_dataframe(opt)
    modelo = dataframe_to_model(df, PcapInfo)
