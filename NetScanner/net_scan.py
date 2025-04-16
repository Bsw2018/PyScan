# This class is a scanner for detecting the network information from the operating system
# The class name is NetScanner
# The class should look for network interfaces, ip addresses, open ports, firewall rules, etc

import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
import psutil
import socket


class NetScanner:

    def __init__(self):
        self.netInterfaces = self.scan_interfaces() # This is a dictionary of interfaces

    # Returns the dictionary of network interfaces and their family of addresses
    def get_netInterfaceDict(self):
        return self.netInterfaces



    # Method for scanning network interfaces
    def scan_interfaces(self):
        netInterfaces = psutil.net_if_addrs() # Returns a dictionary with the keys being the interface names and the values being address, netmask, netaddress family, etc
        return netInterfaces

    # Method for scanning open ports on the host ip addresses
    def scan_ports(self, host, ports=range(1,10000)):
        open_ports = []
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            try:
                result = s.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
                s.close()
            except socket.error:
                pass
        return open_ports
        
    
    def output_to_file(self, filename="net_scan_output.json"):
        result = {}

        for iface, addr_list in self.netInterfaces.items():
            iface_info = []

            for addr in addr_list:
                if addr.family == socket.AF_INET:  # Only scan IPv4 addresses
                    open_ports = self.scan_ports(addr.address)
                    iface_info.append({
                        "family": str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast,
                        "open_ports": open_ports
                    })
                else:
                    iface_info.append({
                        "family": str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast
                    })

            result[iface] = iface_info

        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)

        #print(f"Network scan output written to {filename}")





def main():

    netscanner = NetScanner()

    netscanner.output_to_file("net_scan_output.json")

if __name__ == "__main__":
    main()



    # # Tester for returning interface names
    # for key, values in netscanner.get_netInterfaceDict().items():
    #     print(key)
    #     #print("Interface Name:" + key)
    #     #print("Interface Details:")
    #     for value in values:
    #         print(value[1])
