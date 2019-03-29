#!/usr/bin/env python

import subprocess
import optparse

def get_arguments():
#making a parser object
    parser = optparse.OptionParser()
    parser.add_option("--interface", "-i", dest = "interface", help = "Interface of which the MAC is to be changed")
    parser.add_option("--mac", "-m", dest = "new_mac", help = "New MAC address")
    (options, arguments) = parser.parse_args()
#setting up errors
    if not options.interface:
        parser.error("No interface specified, use --help for more info")
    if not options.new_mac:
        parser.error("New MAC address not specified, use --help for more info")
    return options

def mac_changer(interface, mac_address):
    print("Changing mac adress for " + interface + " to " + mac_address)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

options = get_arguments()
mac_changer(options.interface,options.new_mac)
