import sys
import getopt
import time
from os import popen
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp, IP, UDP, Ether, TCP, ICMP
from random import randrange
import random
from py_essentials import simpleRandom
import socket
def generateSourceIP():
    #not valid for first octet of IP address
    not_valid = [10, 127, 254, 1, 2, 169, 172, 192]

    #selects a random number in the range [1,256)
    first = randrange(1, 256)

    while first in not_valid:
        first = randrange(1, 256)

    #eg, ip = "100.200.10.1"
    ip = ".".join([str(first), str(randrange(1,256)), str(randrange(1,256)), str(randrange(1,256))])

    return ip

#start, end: given as command line arguments. eg, python traffic.py -s 2 -e 65
def generateDestinationIP(start, end):
    first = 10
    second = 0;
    third = 0;

    #eg, ip = "10.0.0.64"
    ip = ".".join([str(first), str(second), str(third), str(randrange(start,end))])

    return ip

def main(argv):
    #print argv

    #getopt.getopt() parses command line arguments and options
    try:

        opts, args = getopt.getopt(sys.argv[1:], 's:e:', ['start=','end='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt =='-s':
            start = int(arg)
        elif opt =='-e':
            end = int(arg)

    if start == '':
        sys.exit()
    if end == '':
        sys.exit()

    #open interface eth0 to send packets
    # interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
    # print("interface: {0}, rstrip: {1}".format(interface,interface.rstrip()))
    table={num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
    interface = "nat0-eth0"
    for i in xrange(100):
        randd = random.random()
        srcip = generateSourceIP ()
        dstip = generateDestinationIP (start, end)
        if randd >= 0.5: 
            packets = Ether() / IP(dst = dstip, src =srcip) / TCP(dport = 80, sport = 20) / str(simpleRandom.randomString(random.randint(0,1300)))
            # print(table[packets.proto],packets.src,packets.dst)
            print((repr(packets)[:81]))
            sendp(packets, iface = interface.rstrip(), inter = 0.1,count=random.randint(1,3))
            packets1 = Ether() / IP(dst =  srcip , src =dstip)/ TCP(dport = 80, sport = 20) / str(simpleRandom.randomString(random.randint(0,1300)))
            print((repr(packets1)[:81]))
            sendp(packets1, iface = interface.rstrip(), inter = 0.1,count=random.randint(1,3))
        elif randd < 0.5 and randd >0.3:
            packets = Ether() / IP(dst = dstip, src =srcip) / UDP(dport = 80, sport = 20) / str(simpleRandom.randomString(random.randint(0,1000)))
            print((repr(packets)[:81]))
            sendp(packets, iface = interface.rstrip(), inter = 0.1,count=random.randint(1,3))
            packets1 = Ether() / IP(dst =  srcip , src =dstip)/ UDP(dport = 80, sport = 20) / str(simpleRandom.randomString(random.randint(0,900)))
            print((repr(packets1)[:81]))
            sendp(packets1, iface = interface.rstrip(), inter = 0.1,count=random.randint(1,3))
        else:
            packets = Ether() / IP(dst = dstip, src =srcip) / ICMP() / str(simpleRandom.randomString(random.randint(0,700)))
            print((repr(packets)[:81]))
            sendp(packets, iface = interface.rstrip(), inter = 0.1,count=random.randint(1,3))
            packets1 = Ether() / IP(dst =  srcip , src =dstip)/ ICMP() / str(simpleRandom.randomString(random.randint(0,600)))
            print((repr(packets1)[:81]))
            sendp(packets1, iface = interface.rstrip(), inter = 0.1,count=random.randint(1,3))
if __name__ == '__main__':
  main(sys.argv)
