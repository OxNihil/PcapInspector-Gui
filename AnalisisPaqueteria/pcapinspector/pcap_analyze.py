def generate_csv(pcap_file):
	f_in = pcap_file
	f_out = "tmp.csv"
	tshark_template = 'tshark -r {} -T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e _ws.col.SrcPort -e _ws.col.DstPort -e ip.proto -e ip.ttl -e _ws.col.Protocol -e ip.len -E header=y -E separator=, -E 		quote=d -E occurrence=f  > {}'
	final_tshark_cmd = tshark_template.format(f_in,f_out)
	os.system(final_tshark_cmd)
	return f_out


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
			ports_src = row["_ws.col.SrcPort"]
			ports_dst = row["_ws.col.DstPort"]
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
#Registro
class opts:
	portFilter = ""
	protoFilter = ""
	pcap_name = ""
