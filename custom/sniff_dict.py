from scapy.all import sniff
from scapy.all import IP
import socket
import time
import pandas as pd

table={num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
count_packets_in_return = 0
dst_bytes = None
dst_ip = None
count = 0
log_file = {}
def checkKey(dict,key,value):
	if str(key) in dict.keys():
		print (" Key has existed!")
	elif "10.0.0." in str(key) and str(key) == str(value["src_ip"]):
		print ("updating")
		src_ip = dict[value["dst_ip"]]["src_ip"]		
		dst_ip = dict[value["dst_ip"]]["dst_ip"]
		src_bytes = dict[value["dst_ip"]]["len"]
		duration = time.time() - dict[value["dst_ip"]]["time"]
		proto = dict[value["dst_ip"]]["proto"]
		dst_bytes = value["len"]
		dict[value["dst_ip"]] = {"src_ip":src_ip,"dst_ip":dst_ip,"duration":duration, "proto":proto ,"src_bytes":src_bytes,"dst_bytes":dst_bytes}
		print(dict[value["dst_ip"]])
	else:
		dict[str(key)] = value
		print("Added a new key")
def custom_action(packet):
	global count_packets_in_return
	global dst_bytes
	global dst_ip
	global log_file
	try:
		print("=============================================")
		print("Src IP: ",packet[IP].src)
		print("Dst IP: ",packet[IP].dst)
		print("Protocol: ",table[packet[IP].proto])
		print("Len: ",packet[IP].len)
		_dict = {"src_ip":packet[IP].src,"dst_ip":packet[IP].dst,"proto":table[packet[IP].proto],"len":packet[IP].len,"time":time.time()}
		checkKey(log_file,packet[IP].src,_dict)
	except IndexError:
		pass
print(sniff(iface="nat0-eth0",prn= custom_action, store=0 ))