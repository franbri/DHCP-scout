import os
import argparse
import fileMan
import time

from scapy.all import sniff, conf, get_if_hwaddr, get_if_list, get_if_addr, AsyncSniffer

if os.name == 'nt':
    from scapy.all import get_windows_if_list as _get_if_list
elif os.name == 'posix':
    from scapy.all import get_if_list as _get_if_list

from scapy import layers

from common import Host, PACKETS_WITHOUT_DHCP, get_requested_address, get_hostname
from utils import get_time, check_port_open


def packetHandler(packet):
    try:
        source_mac = packet.getlayer(layers.l2.Ether).src
        dest_mac = packet.getlayer(layers.l2.Ether).dst
    except:
        return

    ip_layer = packet.getlayer(layers.inet.IP)

    if not ip_layer:
        return

    source_ip = ip_layer.src
    dest_ip = ip_layer.dst

    host = Host(source_mac)
    host.set_ip(source_ip)

    # more unique identifier
    host = known_hosts.setdefault(host.mac, host)
    host.increase_packet_num()

    dhcp_layer = packet.getlayer(layers.dhcp.DHCP)

    if dhcp_layer:
        try:
            requested_address = get_requested_address(dhcp_layer)
            hostname = get_hostname(dhcp_layer)
        except ValueError:
            print('Caught non-DCHPREQUEST packet')
            return

        host.set_ip(requested_address)
        host.set_hostname(hostname)
        host.set_dhcp_seen()

    #now = get_time()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface',
                        help='specify interface to work with')
    parser.add_argument('--show-interfaces', action='store_true',
                        help='get list of all available ifaces')
    args = parser.parse_args()

    interface = args.interface or conf.iface
    interface_hwaddr = get_if_hwaddr(interface)

    try:
        known_hosts = fileMan.loadState()
    except:
        known_hosts = {}

    sniffer = AsyncSniffer( iface=args.interface,
                    filter="(port 67 or 68) or (net 192.168.1.0/24)",
                    prn=packetHandler, store=0)
    sniffer.start()

    while True:
        '''sniff(count=1000, iface=args.interface,
                       filter="net 192.168.1.0/24 or (port 67 or 68)",
                       lfilter=lambda d: d.src != interface_hwaddr,
                       prn=packetHandler)
                       '''
        temp_dict = known_hosts.copy()
        time.sleep(30)
        fileMan.saveState(temp_dict)
        dhcpFile = open('dhcp.leases', 'w')

        for entry in temp_dict.values():
            if entry.broadcasted_dhcp == True:
                dhcpFile.write(entry.to_lease())