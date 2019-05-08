from scapy.all import sniff
from scapy.all import IP
import socket
import time
import pandas as pd
import numpy as np
import datetime
import os
import traceback
import logging
import random

table={num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
log_file = {}
time_log = {}
count = 0
def forNow(dict):
	for key in dict.keys():
		if time.time() - key >= 2:
			del dict[key]
	_list = []
	for key,value in dict.iteritems():
		_list += value
	return _list

def save_log_file(dict,file_name):
	for key,value in dict.iteritems():
		if "time" not in str(value):
			with open(file_name,'a') as the_file: 
				the_file.write(str(str(value['duration'])+ "\t"+str(value['proto'])+ "\t"+str(value['src_bytes'])+ "\t"+str(value['dst_bytes'])+ "\t"+str(value['src_count'])+ "\t"+str(value['dst_count'])+"\n"))
		else:
			with open("error_"+str(file_name),'a') as the_file: 
				the_file.write(str(str(value['time'])+ "\t"+str(value['proto'])+ "\t"+str(value['len'])+ "\t"+str(0)+ "\t"+str(random.randint(0,16))+ "\t"+str(random.randint(0,14))+"\n"))

def checkKey(dict,key,value,_list_2_sec):
	try:
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
			dict[value["dst_ip"]] = {"duration":duration, "proto":proto ,"src_bytes":src_bytes,"dst_bytes":dst_bytes,"src_count":src_count,"dst_count":dst_count}
		else:
			dict[str(key)] = value
			print("Added a new key")
		now = datetime.datetime.now()
		time_stop = datetime.datetime.now().replace(day=9,hour=10, minute=54,second=10, microsecond=0)
		print ("time_now: ",now)
		if now >= time_stop:
			save_log_file(dict,file_name= "last_file.txt")
			print("Time has been counted!")
			os._exit(0)
	except Exception as e:
		print ("\nException, Error!")
def custom_action(packet):
	# try:
	global log_file
	global time_log
	global count
	try:
		print("=============================================")
		print("Src IP: ",packet[IP].src)
		print("Dst IP: ",packet[IP].dst)
		time_log[time.time()] = [packet[IP].src,packet[IP].dst]
		list_2_sec = forNow(time_log)
		_dict = {"src_ip":packet[IP].src,"dst_ip":packet[IP].dst,"proto":table[packet[IP].proto],"len":packet[IP].len,"time":time.time()}
		checkKey(log_file,packet[IP].src,_dict,list_2_sec)
		if len(log_file) % 1000 == 0 and len(log_file) != 0:
			count+=1
			save_log_file(log_file,file_name= "save_file_"+str(count)+".txt")
			print("Save batch file: ",count)
	except IndexError:
		pass
	# except Exception as e:
	# 	print("======================= Exception ======================")
	# 	save_log_file(log_file,file_name= "exception_file.txt")
	# 	print("time up!")
	# 	os._exit(0)
	# 	print(logging.error(traceback.format_exc()))
print(sniff(iface="nat0-eth0",prn= custom_action, store=0 ))