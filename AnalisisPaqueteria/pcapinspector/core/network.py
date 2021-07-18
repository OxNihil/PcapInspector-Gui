from scapy.all import *
from scapy.layers import http

#Registro2
class data_analyze():
	def __init__(self):
		self.gateway = ""
		self.vlans = []
		self.netbios = {}
		self.root_bridge = ""
		self.user_agents = []
		self.servers = []
		self.dnsqd = []
		self.dnsan = {}
		self.alerts = []

class analyze_scapy():
	def __init__(self,pcap_file):
		self.file = pcap_file
		self.packets = rdpcap(pcap_file) 
		self.data = data_analyze()
	def fast_scan(self):
		for packet in self.packets:
			self.try_guess_gw(packet)
			self.check_for_vlans(packet)
			self.check_for_netbios(packet)
			self.check_for_rootbridge(packet)
			self.check_http_data(packet)
			self.check_for_dns(packet)
			#Añadir funciones...
		return self.data
	def try_guess_gw(self,packet):
		#Si se captura una petición DHCP
		if packet.haslayer(DHCP):
			dhcp_opts = packet[DHCP].fields['options']
			for i in dhcp_opts:
				if i[0] == "router" and self.data.gateway == "":
					self.data.gateway = i[1]
					break
		#Con paquete IGMP
		if packet.haslayer(IP):
			#IGMPv3
			if packet[IP].proto == 2:
				self.data.gateway = packet[IP].src
	def check_for_vlans(self,packet):
		if packet.haslayer(Dot1Q):
			vlan = packet[Dot1Q].vlan
			if vlan not in self.data.vlans:
				self.data.vlans.append(vlan)
	def check_for_netbios(self,packet):
		#NBT - NETBIOS over Tcp
		if packet.haslayer(NBTDatagram):
			fields = packet[NBTDatagram].fields
			sip = fields['SourceIP']
			sname = fields['SourceName'].decode("utf-8",errors="ignore")
			self.data.netbios[sip] = sname
	def check_for_rootbridge(self,packet):
		if packet.haslayer(STP):
			pf = packet.fields
			stpfield = packet[STP].fields
			if 'rootmac' in stpfield:
				self.data.root_bridge = stpfield['rootmac']
	def check_http_data(self,packet):
		if packet.haslayer(http.HTTPRequest):
			msg = packet[http.HTTPRequest].fields
			if "User_Agent" in msg.keys():
				user_agent = str(msg['User_Agent'].decode("utf-8",errors="ignore"))
				print(user_agent)
				if user_agent not in self.data.user_agents:
					self.data.user_agents.append(user_agent)
		elif packet.haslayer(http.HTTPResponse):
			msg = packet[http.HTTPResponse].fields
			if "User_Agent" in msg.keys():
				user_agent = str(msg['User_Agent'].decode("utf-8",errors="ignore"))
				print(user_agent)
				if user_agent not in self.data.user_agents:
					self.data.user_agents.append(user_agent)
			if "Server"  in msg.keys():
				server = str(msg['Server'].decode("utf-8",errors="ignore"))
				if server not in self.data.servers:
					self.data.servers.append(server)
		elif packet.haslayer(Raw):
			if "HTTP" in str(packet[Raw].load):
				http_data = packet[Raw].load.decode("utf-8",errors="ignore").split("\r\n")
				for i in http_data:
					if "User-Agent:" in i and i not in self.data.user_agents:
						self.data.user_agents.append(i)
					if "Server" in i and i not in self.data.servers:
						self.data.servers.append(i)
	def check_for_dns(self,packet):
		try: 
			if packet.haslayer(DNS):
				qd = packet[DNS].qdcount
				an = packet[DNS].ancount
				#Answer records
				if an > 0:
					anfields = packet[DNS].an.fields
					for x in range(an):
						if packet.haslayer("DNSRRSOA"):
							if packet[DNSRRSOA][x].type == 1:
								rdata = packet[DNSRRSOA][x].rdata
								rtype = packet[DNSRRSOA][x].type
								rrname = packet[DNSRRSOA][x].rrname.decode('utf-8')
								self.data.dnsan[rdata] = anfields['rrname'].decode('utf-8')
								rec = rdata +" "+rrname +" "+ str("")
								if rec not in self.data.dnsqd:
									self.data.dnsqd.append(rec)
							elif packet.haslayer("DNSRR"):
								if packet[DNSRR][x].type == 1:
									rdata = packet[DNSRR][x].rdata
									rtype = packet[DNSRR][x].type
									rrname = packet[DNSRR][x].rrname.decode('utf-8')
									self.data.dnsan[rdata] = anfields['rrname'].decode('utf-8')
									rec = rdata +" "+rrname +" "+ str("A")
									if rec not in self.data.dnsqd:
										self.data.dnsqd.append(rec)
				#Question records
				if qd > 0:
					qdfields = packet[DNS].qd.fields
					name = qdfields['qname'].decode("utf-8",errors="ignore")
					if name not in self.data.dnsqd:
						self.data.dnsqd.append(name)
					#Detect Zone transfer
					if (str(qdfields['qtype']) == "252"):
						msg = "[+]ALERT DNS: Zone transfer axfr"
						self.data.alerts.append(msg)
					elif (str(qdfields['qtype']) == "251"):
						msg = "[+]ALERT DNS: Zone transfer ixfr"
						self.data.alerts.append(msg)
		except Exception as e:
			print(e)
			pass
			
class net():
	def return_ttl_so_name(self,ttl_number):
		ttl_number = int(ttl_number)
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
