from scapy.all import *
from scapy.layers import http

#Registro2
class data_analyze():
	def __init__(self):
		self.gateway = ""
		self.vlans = []
		self.netbios = {}
		

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
