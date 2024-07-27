from scapy.all import *
import datetime


PACKETS_WITHOUT_DHCP = 5
LEASE_TIME = 28800

class Host:
    def __init__(self, mac: str):
        self._mac = mac
        self._hostname = None

        self._ip = None
        self._broadcasted_dhcp = False
        self._num_packets = 0
        self._seen = False
        self._dhcp_lease_start = None
        self._dhcp_lease_end = None

    def increase_packet_num(self) -> None:
        self._num_packets += 1

    def set_seen(self) -> None:
        self._seen = True

    def set_dhcp_seen(self) -> None:
        self._dhcp_lease_start = datetime.datetime.now()
        self._dhcp_lease_end = self._dhcp_lease_start + datetime.timedelta(0, LEASE_TIME)
        self._broadcasted_dhcp = True
    
    def set_hostname(self, hostname) -> None:
        self._hostname = hostname

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def ip(self):
        return self._ip

    def set_ip(self, ip) -> None:
        self._ip = ip

    @property
    def broadcasted_dhcp(self) -> bool:
        return self._broadcasted_dhcp

    @property
    def num_packets(self):
        return self._num_packets

    @property
    def seen(self):
        return self._seen

    def __repr__(self):
        return '{} @ {} | DHCP seen: {}'.format(self.mac, self.ip,
                                              self.broadcasted_dhcp)
    
    def to_lease(self):
        start_date = self._dhcp_lease_start.strftime("%w %Y/%m/%d %H:%M:%S")
        end_date = self._dhcp_lease_end.strftime("%w %Y/%m/%d %H:%M:%S")
        if self._hostname != None:
            return 'lease {} {{\n\tstarts {};\n\tends {};\n\thardware ethernet {};\n\tclient-hostname "{}";\n\tbinding state {};\n\t}}'.format(self._ip, start_date,
                                                                                                                                           end_date, self._hostname,
                                                                                                                                             "free")
        else:
            return 'lease {} {{\n\tstarts {};\n\tends {};\n\thardware ethernet {};\n\tbinding state {};\n\t}}'.format(self._ip, start_date,
                                                                                                                      end_date, "free")


# Fixup function to extract dhcp_options by key
def get_option(dhcp_options, key):
    must_decode = ['hostname', 'domain', 'vendor_class_id']
    try:
        for i in dhcp_options:
            if i[0] == key:
                # If DHCP Server Returned multiple name servers
                # return all as comma seperated string.
                if key == 'name_server' and len(i) > 2:
                    return ",".join(i[1:])
                # domain and hostname are binary strings,
                # decode to unicode string before returning
                elif key in must_decode:
                    return i[1].decode()
                else:
                    return i[1]
    except:
        pass


def get_requested_address(packet):
    if packet.options[0][1] != 3:
        raise ValueError('Packet {} is not DHCPREQUEST'.format(packet))

    requested_address = get_option(packet.options, 'requested_addr')
    return requested_address

def get_hostname(packet):
    if packet.options[0][1] != 3:
        raise ValueError('Packet {} is not DHCPREQUEST'.format(packet))

    requested_address = get_option(packet.options, 'hostname')
    return requested_address
