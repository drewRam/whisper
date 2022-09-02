import socket
import subprocess
import ipaddress
import re
import threading

from queue import Queue

THREAD_POOL_SIZE = 100
ENDPOINT_ADDR = ("8.8.8.8", 80)
IP_PATTERN = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

def get_net_from_ipconfig() -> (str, str):
	output = subprocess.run("ipconfig", stdout=subprocess.PIPE).stdout
	output = output.decode()

	ip = ""
	subnet = ""

	for line in output.split("\r\n"):
		if "IPv4" in line:
			ip = re.search(IP_PATTERN, line).group(1)
		elif "Subnet" in line:
			subnet = re.search(IP_PATTERN, line).group(1)
	
	return ip, subnet

def get_set_bits(subnet: str) -> int:
	set_bits = 0
	for octet in subnet.split('.'):
		if octet == "255":
			set_bits += 8
		else:
			octet = int(octet)
			i = 7
			
			while octet > 0:
				if octet >  2**i:
					octet -= 2**i
					set_bits += 1

				i -= 1

	return set_bits


def get_network_ip_address(client_ip: str, netmask:str) -> str:
	result = []
	
	for ip_octet, sub_octet in zip(client_ip.split("."), netmask.split(".")):
		ip_octet = int(ip_octet)
		sub_octet = int(sub_octet)

		if sub_octet == 255:
			result.append(str(ip_octet))
		elif sub_octet == 0:
			result.append(str(0))
		else:
			or_val = 0
			
			for i in range(7, -1, -1):
				if ip_octet >= 2**i and sub_octet >= 2**i:
					or_val += 2**i
					ip_octet -= 2**i
					sub_octet -= 2**i
				elif ip_octet >= 2**i:
					ip_octet -= 2**i
				elif sub_octet >= 2**i:
					sub_octet -= 2**i
					
					if sub_octet == 0:
						break

			result.append(str(or_val))

	return '.'.join(result) + '/' + str(get_set_bits(netmask))