#!/usr/bin/env python3

import subprocess
import ipaddress
import yaml #apt install python3-yaml
import socket
import sys
import logging
from time import sleep

yml_config = "/etc/nut/wakeonlan/config.yml"
pullrate = 10

# --------------------------------------------------- Logging Setup --------------------------------------------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

log = logging.getLogger("power_up")

#---------------------------------------------------Variables---------------------------------------------------#

def get_ups_data (ups_name, nut_ip, parameter):

    #If UPS IP is IPv6, wrap it in [] (required by upsc)
    try:
        ip_addr = ipaddress.ip_address(nut_ip)
        if (ip_addr.version == 6):
            if not (nut_ip.startswith("[") and nut_ip.endswith("]")):
                nut_ip = f"[{nut_ip}]"
    except ValueError:
        pass #To pass hostnames

    # Read the data from the UPS and return it
    command = ["upsc", f"{ups_name}@{nut_ip}", parameter]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError while reading ups data: {e}\033[0m")
        log.error(f"Error while reading ups data: {e}")
        print(f"\033[33mTry checking the UPS name and IP address\033[0m")
        log.info("Try checking the UPS name and IP address")
        sys.exit(1)


def wake_on_lan (mac_address, ip_version, ipv6_interface=None):

    mac_address2 = mac_address.replace(":", "").replace ("-", "")
    if (len(mac_address2) != 12):
        print(f"\033[91mError: '{mac_address}' is not a valid mac address. Use the notation: '00:00:00:00:00:00' or '00-00-00-00-00-00'\033[0m")
        log.error(f"'{mac_address}' is not a valid mac address. Use the notation: '00:00:00:00:00:00' or '00-00-00-00-00-00'")
        sys.exit(1)

    #Create and send magic packet for Wake-on-LAN over IPv6
    if (ip_version == "ipv6"):
        
        #Error if no IPv6 interface was specified
        if (not ipv6_interface):
            print("\033[91mError: IPv6 wake on lan requires an interface (e.g. 'eth0')\033[0m")
            log.error("IPv6 wake on lan requires an interface (e.g. 'eth0')")
            sys.exit(1)

        try:
            if_index = socket.if_nametoindex(ipv6_interface)
        except OSError:
            print(f"\033[91mError: Interface {ipv6_interface} does not exist\033[0m")
            log.error(f"Interface {ipv6_interface} does not exist")
            sys.exit(1)

        #Build and send the magic packet
        data = b'\xff' * 6 + bytes.fromhex(mac_address2) * 16
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        dest = ("ff02::1", 9, 0, if_index)
        sock.sendto(data, dest)
        sock.close()

    #Create magic packet for Wake-on-LAN over IPv4
    elif (ip_version == "ipv4"):
       
        #Build and send the magic packet
        data = b'\xff' * 6 + bytes.fromhex(mac_address2) * 16
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(data, ('255.255.255.255', 9))
    
    #Error if the given IP version is not valid
    else:
        print(f"\033[91mError: {ip_version} is not a valid ip version. Try using 'ipv6' or 'ipv4'\033[0m")
        log.error(f"{ip_version} is not a valid ip version. Try using 'ipv6' or 'ipv4'")
        sys.exit(1)



#---------------------------------------------------Functions---------------------------------------------------#

def main():
    #Read configuration from YAML file
    try:
        with open (yml_config, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"\033[91mError: Config file not found: {yml_config}\033[0m")
        log.error(f"Config file not found: {yml_config}")
        sys.exit(1)

    ups_name = config["nut"]["ups_name"]
    ups_ip = config["nut"]["ip"]
    wol_list = config["wol"]

    #Last reported UPS status (from NUT)
    last_ups_status = get_ups_data(ups_name, ups_ip, "ups.status").split()
    print(f"Info: Initial UPS status: {' '.join(last_ups_status)}")
    log.info(f"Initial UPS status: {' '.join(last_ups_status)}")

    print("Info: Starting monitoring UPS...")
    log.info("Starting monitoring UPS...")

    try:
        while True:
            #Query UPS status using get_ups_data()
            status = get_ups_data(ups_name, ups_ip, "ups.status")
            if status:
                flags = status.split()
                
                #Log UPS status only if it has changed
                if flags != last_ups_status:
                    print(f"Info: UPS status changed to: {' '.join(flags)}")
                    log.info(f"UPS status changed to: {' '.join(flags)}")

                #If UPS changes status from On Battery (OB) or Low Battery (LB) to Online (OL)
                if (last_ups_status and any(x in last_ups_status for x in ["OB", "LB"]) and "OL" in flags):
                    
                    print("\033[92mPower restored! Waking up clients...\033[0m")
                    log.info("Power restored! Waking up clients...")
                    
                    #Send magic packets to all clients defined in the YAML file
                    for client in wol_list:
                        ip_version = "ipv6" if client["ip_version"] == 6 else "ipv4"
                        wake_on_lan(client["mac"], ip_version, client.get("interface"))
                        print(f"Sent WOL packet to {client['mac']} ({ip_version})")
                        log.info(f"Sent WOL packet to {client['mac']} ({ip_version})")

                last_ups_status = flags

            #If no status was returned, print an error and exit
            else:
                print("\033[91mAn unknown error occurred while trying to read UPS data\033[0m")
                log.info("An unknown error occurred while trying to read UPS data")
                sys.exit(1)

            sleep(pullrate)

    except KeyboardInterrupt:
        print ("\nExiting...")


if __name__ == "__main__":
    main()
