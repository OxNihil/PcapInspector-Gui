def generate_dataframe(pcap_file):
    f_in = pcap_file
    f_out = "tmp.csv"
    tshark_template = 'tshark -r {} -T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ' \
                      '_ws.col.SrcPort -e _ws.col.Dport -e ip.ttl -e _ws.col.Protocol -e ip.len -E header=y -E separator=, -E quote=d -E occurrence=f > {}'
    tshark_command = tshark_template.format(f_in, f_out)
    os.system(tshark_command)
    return pd.read_csv("tmp.csv")