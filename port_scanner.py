#!/bin/python3

#Ports 53, 80, etc are usually open

#TODO : Multithreading

import sys
import optparse
import socket

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("--ip","-i",dest = "ip", help = "IP Address")
    parser.add_option("--port","-p",dest = "port", help = "Port No.")
    options, arguments = parser.parse_args()
    if not options.ip:
        parser.error("IP Address not specified")

    return options

def check_port(port_no):
    #AF_INET -> IPv4, SOCK_STREAM -> Port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #wait for 1 second and move on if connection is not made
    socket.setdefaulttimeout(1)
    exit_status = s.connect_ex((ip,port_no))
    if exit_status == 0:
        print("Port {} is open".format(port_no))
    s.close()
    return

options = get_arguments()
ip = socket.gethostbyname(options.ip)
#gethostbyname will convert machine hostname to IP if necessary
print("Scanning " + ip)
if options.port:
    check_port(int(options.port))

if not options.port:
    try:
        for port in range(1,1000):
            check_port(port)
    except KeyboardInterrupt:
        print("Exiting program after checking first {} ports".format(port))
        sys.exit()
    except socket.gaierror:
        print("Hostname couldn't be resolved to an IP. Try enting an IP Address directly")
        sys.exit()
    except socket.error:
        print("A connection to the server could not be established")
        sys.exit()
    except:
        print("An unknown error occured")
        sys.exit()
