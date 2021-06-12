import pandas as pd
import numpy as np
import os
from .generate_csv import dataframe_to_model, model_to_dataframe
from AnalisisPaqueteria.pcapinspector.models import *
import matplotlib.pyplot as plt


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
        all_ips = df["ip_src"].dropna().unique()
        all_ips = list(dict.fromkeys(all_ips))
        return all_ips

    def get_endpoints_mac(self):
        all_mac = df["eth.src"].dropna().unique()
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

    def func(self, pct, allvals):
        absolute = int(round(pct / 100. * np.sum(allvals)))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    def stats(self, column, title, legend):
        valor = 3  # numero de items que queremos mostrar en la leyenda de forma independiente
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        data = df[column].value_counts()
        protocols, values = data.index.tolist(), data.tolist()
        protocols_toprint, values_toprint = protocols[:valor], values[:valor]
        if len(values) > valor:
            protocols_toprint.append("Others: " + str(protocols[valor:len(protocols)]))

            values_toprint.append(np.sum(values[valor:len(values)]))

        wedges, texts, autotexts = ax.pie(values_toprint,
                                          autopct=lambda pct: analyze_dataframe(df).func(pct, values_toprint),
                                          textprops=dict(color="w"))
        ax.legend(wedges, protocols_toprint,
                  title=legend,
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title(title)
        # analyze_dataframe(df).stats('_ws.col.Protocol', "Listado de protocolos", "Protocolos")
        plt.savefig(legend + ".png")


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
