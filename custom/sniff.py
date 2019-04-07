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
def custom_action(packet):
	global count_packets_in_return
	global dst_bytes
	global dst_ip
	global count
	try:
		start = time.time()
		print("=============================================")
		print("Src IP: ",packet[IP].src)
		print("Dst IP: ",packet[IP].dst)
		print("Protocol: ",table[packet[IP].proto])
		print("Len: ",packet[IP].len)
		print("Time = ",time.time()-start)
		count_packets_in_return += 1
		print("count_packets_in_return: ",count_packets_in_return)
		src_ip = packet[IP].src
		src_bytes = packet[IP].len
		proto = table[packet[IP].proto]
		count+=1
		if dst_ip == None:
			dst_ip = packet[IP].dst
			dst_bytes = packet[IP].len
		print (src_ip,"\t",dst_ip)
		if src_ip == dst_ip and "10.0.0"  in str(src_ip) :
			print("Writing matching ip")
			with open("log_file.txt",'a') as the_file:
				the_file.write(str(str(packet[IP].dst) + "\t" + str(packet[IP].src) + "\t" + str(time.time()-start) + "\t" + str(proto) + "\t" + str(dst_bytes)  + "\t" + str(src_bytes) + "\n"))
			count = 0
			dst_ip = None
			dst_bytes = None
		elif count >=5 and  "10.0.0" in src_ip:
			print("Writing no matching ip")
			with open("log_file.txt",'a') as the_file:
				the_file.write(str(str(packet[IP].dst) + "\t" + str(packet[IP].src) + "\t" + str(time.time()-start) + "\t" + str(proto) + "\t" + str(dst_bytes)  + "\t" + str(0) + "\n"))
			count = 0
			dst_ip = None
			dst_bytes = None
	except IndexError:
		pass
print(sniff(iface="nat0-eth0",prn= custom_action, store=0 ))