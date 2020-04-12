#!/usr/bin/env python
# When "SIOCSIFHWADDR: Cannot assign requested address" Error is experienced, Change the first octet to an  even Value. This is because the cmaand accepts only unicast address.
# This Mac Changer script is made immune to commmand injection attacks to my knowledge. So you can allow this Script to run as root without password for regular users.

import subprocess
import argparse
import re
from termcolor import colored

def get_arguements():
    parser = argparse.ArgumentParser() # Anything that starts with Caps refers to a Class [It's a naming Convention]
    parser.add_argument("-i", "--interface", dest="interface", help = "Interface to Change the Mac Address on.")
    parser.add_argument("-m", "--mac", dest="mac", help = "New Mac Address.")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] NO Interface specified. Use -h or --help for more info.")
    elif not options.mac:
        parser.error("[-] NO Mac Address specified. Use -h or --help for more info.")
    return options

def change_mac(interface, mac):
    print(colored(f"[+] Changing Mac Address to {mac} on {interface}", "green"))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac(interface):
    ifconfig = (subprocess.check_output(["ifconfig", interface])).decode()
    mac_address = (re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)).group(0)
    if mac_address:
        return mac_address
    else:
        print(colored("[-] Couldn't read Mac Address", "red"))

def check_mac(current_mac, mac):
    if current_mac == mac:
        print(colored(f"[+] Mac Address Changed to {current_mac}", "green"))
    else:
        print(colored("[-] Mac Address not Changed. ", "red"))

options = get_arguements()
change_mac(options.interface, options.mac)
current_mac = get_mac(options.interface)
check_mac(current_mac, options.mac)