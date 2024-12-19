#Đây là nơi thực hiện các phép tính liên quan đến IPv4, subnet và regex.


import ipaddress
import re

def calculate_ipv4(ipv4):
    try:
        ip = ipaddress.ip_address(ipv4)
        return {
            'address': str(ip),
            'is_private': ip.is_private,
            'is_global': ip.is_global
        }
    except ValueError:
        return 'Invalid IPv4 address'

def calculate_subnet(network):
    try:
        net = ipaddress.ip_network(network, strict=False)
        return {
            'network_address': str(net.network_address),
            'netmask': str(net.netmask),
            'broadcast_address': str(net.broadcast_address),
            'num_addresses': net.num_addresses
        }
    except ValueError:
        return 'Invalid network'

def validate_regex(regex, text):
    matches = re.findall(regex, text)
    return {
        'matches': matches,
        'num_matches': len(matches)
    }
