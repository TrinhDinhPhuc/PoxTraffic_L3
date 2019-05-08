from scapy.all import sniff

pkts = sniff(iface="nat0-eth0")
print("pkts :",pkts)
for pkt in pkts:
	print("pkt= ",pkt.time)from scapy.all import sniff
    