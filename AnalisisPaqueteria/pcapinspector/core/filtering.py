import base64
import networkx as nx
import pandas as pd
import numpy as np
import os
from pcapinspector.models import PcapInfo
import matplotlib.pyplot as plt

plt.switch_backend('agg')
from matplotlib.lines import Line2D
from django.conf import settings
from io import StringIO, BytesIO
from .network import net


class analyze_dataframe():
    def __init__(self, df):
        self.df = df
    def get_endpoints_ip(self):
        all_ips = self.df["ip_src"].dropna().unique()
        all_ips = list(dict.fromkeys(all_ips))
        return all_ips
    def get_endpoints_ip_dst(self):
        all_ips = self.df["ip_dst"].dropna().unique()
        all_ips = list(dict.fromkeys(all_ips))
        return all_ips
    def get_endpoints_proto(self):
    	all_proto = self.df["protocol"].dropna().unique()
    	all_proto = list(dict.fromkeys(all_proto))
    	return all_proto
    def get_endpoints_mac(self):
        all_mac = self.df["eth_src"].dropna().unique()
        all_mac = list(dict.fromkeys(all_mac))
        return all_mac
    def get_endpoints_mac_dst(self):
        all_mac = self.df["eth_dst"].dropna().unique()
        all_mac = list(dict.fromkeys(all_mac))
        return all_mac
    def get_endpoints_port(self):
        all_port = self.df[self.df['src_port'] <= 49152]["src_port"].dropna().unique()
        all_port = list(dict.fromkeys(all_port))
        return all_port
    def get_endpoints_port_dst(self):
        all_port = self.df[self.df['dst_port'] <= 49152]["dst_port"].dropna().unique()
        all_port = list(dict.fromkeys(all_port))
        return all_port

    def get_endpoints_ttl(self):
        ttls = self.df.groupby(["ip_src"])["ttl"].min()
        return ttls.to_dict()

    def get_endpoints_so(self):
        so = {}
        ttls = self.get_endpoints_ttl()
        for i in ttls:
            so[i] = net().return_ttl_so_name(ttls[i])
        return so

    def create_graph(self):
        G = nx.Graph()
        all_ips = self.df["ip_src"].dropna().unique()
        all_ips = list(dict.fromkeys(all_ips))
        ips_grp = self.df.groupby(["ip_src", "ip_dst"])
        ips_protos = ips_grp["protocol"].unique()
        ips_protos_dst = ips_grp["ip_dst"].unique()
        for i in all_ips:
            # solo almacenamos nodos de ips locales
            if (net().is_local_unicast(str(i))):
                G.add_node(str(i))
            else:
                continue
            # Recorremos el dataframe y obtenemos el dst y protocolos
            for j in range(len(ips_protos[i])):
                proto_ip = ips_protos[i].iloc[j]
                dst_ip = ips_protos_dst[i].iloc[j][0]
                # Comprobamos si la ip de destino es local
                if (net().is_local_net(dst_ip)):
                    if i != j:
                        G.add_edge(i, str(dst_ip), proto=proto_ip)
                # La ip de destino es externa
                G.add_node("Internet")  # WAN
                G.add_edge(i, "Internet", proto=proto_ip)
                # De internet al nodo externo objetivo
                tag = str(proto_ip)
                G.add_edge("Internet", str(dst_ip), proto=tag)
        return G

    def show_graph(self):
        plt.figure(figsize=(12, 7))
        G = self.create_graph()
        pos = nx.spring_layout(G)
        color_map = get_graph_color_map(self.df, G)
        nx.draw_networkx(G, pos, node_color=color_map)
        # legend
        custom_legend = [
            Line2D([0], [0], marker='o', color='w', label='Windows', markerfacecolor='blue', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='Linux', markerfacecolor='orange', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='Uknown', markerfacecolor='gray', markersize=15)]
        # labels
        plt.legend(handles=custom_legend)
        labels = nx.get_edge_attributes(G, 'proto')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        # save graph
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

    def pie_chart(self, column, title, legend):
        valor = 6  # numero de items que queremos mostrar en la leyenda de forma independiente
        fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(aspect="equal"))
        data = self.df[column].value_counts()
        protocols, values = data.index.tolist(), data.tolist()
        protocols_toprint, values_toprint = protocols[:valor], values[:valor]
        if len(values) > valor:
            # protocols_toprint.append("Others: " + str(protocols[valor:len(protocols)]))
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
        # plt.savefig(legend + ".png")
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        data = buffer.getvalue()
        graph = base64.b64encode(data)
        graph = graph.decode('utf-8')
        buffer.close()
        plt.close()
        return graph

    def hist(self):
        # Plot and retrieve the axes
        df = self.df[['protocol', 'ip_len']]
        df = df.groupby(['protocol', 'ip_len']).count().reset_index()
        axes = df.hist(by='protocol', figsize=(12, 6))

        # Define a different color for the first five bars
        colors = ["#00d8ff", "#00b2ff", "#0090ff", "#0f87e4", "#177ecd"]

        for i, ax in enumerate(axes.reshape(-1)):
            # Define a counter to ensure that if we have more than three bars with a value,
            # we don't try to access out-of-range element in colors
            k = 0

            # Optional: remove grid, and top and right spines
            ax.grid(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            for rect in ax.patches:
                # If there's a value in the rect and we have defined a color
                if rect.get_height() > 0 and k < len(colors):
                    # Set the color
                    rect.set_color(colors[k])
                    # Increment the counter
                    k += 1

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        data = buffer.getvalue()
        graph = base64.b64encode(data)
        graph = graph.decode('utf-8')
        buffer.close()
        plt.close()
        return graph

    def lollypop(self, column, title, legend):

        df = self.df.groupby([column]).size().reset_index(name='counts')
        df = df[['counts', column]].groupby(column).apply(lambda x: x.mean())
        max_value = df['counts'].max()

        df.sort_values('counts', inplace=True)
        df.reset_index(inplace=True)

        # Draw plot
        fig, ax = plt.subplots(figsize=(12, 8), dpi=60)
        ax.vlines(x=df.index, ymin=0, ymax=df.counts, color='firebrick', alpha=0.7, linewidth=2)
        ax.scatter(x=df.index, y=df.counts, s=75, color='firebrick', alpha=0.7)

        # Title, Label, Ticks and Ylim
        ax.set_title(title, fontdict={'size': 22})
        ax.set_ylabel(legend)
        ax.set_xticks(df.index)
        ax.set_xticklabels(df[column].str.upper(), rotation=60, fontdict={'horizontalalignment': 'right', 'size': 12})
        # Ajuste de eje y
        ax.set_ylim(0, max_value * 1.1)

        # Annotate
        for row in df.itertuples():
            ax.text(row.Index, row.counts + .5, s=round(row.counts, 2), horizontalalignment='center', verticalalignment='bottom', fontsize=14)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        data = buffer.getvalue()
        graph = base64.b64encode(data)
        graph = graph.decode('utf-8')
        buffer.close()
        plt.close()
        return graph


# AUX FUNS

def get_graph_color_map(df, G):
    color_map = []
    color_lookup = G.nodes()
    knowso = analyze_dataframe(df).get_endpoints_so()
    for i in color_lookup:
        # Asignacion de color a Nodos especiales
        if i == "Internet":
            color_map.append("red")
            continue
        if i == "localhost":
            color_map.append("gray")
            continue
        # ttl_so
        if i in knowso.keys():
            if knowso[i].lower() == "linux":
                color_map.append("orange")
                continue
            elif knowso[i].lower() == "windows":
                color_map.append("blue")
                continue
        color_map.append("gray")
    # Comprobacion por si error
    check = False
    while len(color_map) != len(color_lookup):
        color_map.append("gray")
        check = True
    return color_map
