#!/usr/bin/env python

import scapy.all as scapy
import optparse

def get_ip():
    parser = optparse.OptionParser()
    parser.add_option("--target" , "-t" , dest = "target" , help = "IP value/range to be checked")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("No IP address specified. Please use --help for more info")
    return options.target


def scan(ip):
    arp_request = scapy.ARP()
    #pdst is the field of ip, can use ls with scapy.arp to confirm
    arp_request.pdst = ip
    broadcast = scapy.Ether()
    #dst is the field of the destination mac and ffx6 is the broadcast mac
    broadcast.dst = "ff:ff:ff:ff:ff:ff"
    #combination of the two packets above
    request_all = broadcast/arp_request
    #srp returns 2 values,list of answered packets andlist of unanswered packets; we only need answered hence [0] i.e 1st element
    #false verbose is to instruct srp to not print out shit a user doesn't need
    answered_list = scapy.srp(request_all, timeout = 1, verbose = False)[0]
    #the answered list in itself contains 2 elements, packets sent and the answer
    client_list = []

    for element in answered_list:
        #psrc -> IP; hwsrc -> MAC
        client = {"ip" : element[1].psrc, "mac" : element[1].hwsrc}
        client_list.append(client)
    return client_list

def output(client_list):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in client_list:
        print(client["ip"] + "\t\t" + client["mac"])

ip = get_ip()
clients = scan(ip)
output(clients)
