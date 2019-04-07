from scapy.all import sniff
from scapy.all import IP
import socket
import time
import pandas as pd
import numpy as np
import datetime
import os
table={num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
log_file = {}
time_log = {}
def forNow(dict):
	for key in dict.keys():
		if time.time() - key >= 2:
			del dict[key]
	_list = []
	for key,value in dict.iteritems():
		_list += value
	return _list

def save_log_file(dict):
	for key,value in dict.iteritems():
		if "time" not in str(value):
			with open("log_ffff.txt",'a') as the_file: #str(value['src_ip'])+ "\t"+str(value['dst_ip'])+ "\t"+
				the_file.write(str(str(value['duration'])+ "\t"+str(value['proto'])+ "\t"+str(value['src_bytes'])+ "\t"+str(value['dst_bytes'])+ "\t"+str(value['src_count'])+ "\t"+str(value['dst_count'])+"\n"))

def checkKey(dict,key,value,_list_2_sec):
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
		src_count = 0
		dst_count = 0
		for ip in _list_2_sec:
			if src_ip == ip:
				src_count +=1
			if dst_ip == ip :
				dst_count+=1
		# "src_ip":src_ip,"dst_ip":dst_ip,
		dict[value["dst_ip"]] = {"duration":duration, "proto":proto ,"src_bytes":src_bytes,"dst_bytes":dst_bytes,"src_count":src_count,"dst_count":dst_count}
		print(dict[value["dst_ip"]])
	else:
		dict[str(key)] = value
		print("Added a new key")
	# print (dict)
	now = datetime.datetime.now()
	time_stop = datetime.datetime.now().replace(day=7,hour=20, minute=45, second=0, microsecond=0)
	if now >= time_stop:
		save_log_file(dict)
		print("time up!")
		os._exit(0)

def custom_action(packet):
	global log_file
	global time_log
	try:
		print("=============================================")
		print("Src IP: ",packet[IP].src)
		print("Dst IP: ",packet[IP].dst)
		# print("Protocol: ",table[packet[IP].proto])
		# print("Len: ",packet[IP].len)
		time_log[time.time()] = [packet[IP].src,packet[IP].dst]
		list_2_sec = forNow(time_log)
		# print("Key time number: ",len(time_log))
		_dict = {"src_ip":packet[IP].src,"dst_ip":packet[IP].dst,"proto":table[packet[IP].proto],"len":packet[IP].len,"time":time.time()}
		checkKey(log_file,packet[IP].src,_dict,list_2_sec)
	except IndexError:
		pass
print(sniff(iface="nat0-eth0",prn= custom_action, store=0 ))