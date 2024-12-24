import ipaddress

def calculate_ipv4(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        return {
            "IP Address": str(ip),
            "Is Private": ip.is_private,
            "Is Global": not ip.is_private
        }
    except ValueError:
        return {"error": "Invalid IPv4 address"}

def calculate_ipv6(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        return {
            "IP Address": str(ip),
            "Is Private": ip.is_private,
            "Is Global": not ip.is_private
        }
    except ValueError:
        return {"error": "Invalid IPv6 address"}

def cidr_to_netmask(cidr):
    try:
        network = ipaddress.ip_network('0.0.0.0/' + cidr, strict=False)
        return str(network.netmask)
    except ValueError:
        return None

def netmask_to_cidr(netmask):
    try:
        network = ipaddress.IPv4Network('0.0.0.0/' + netmask, strict=False)
        return str(network.prefixlen)
    except ValueError:
        return None

def calculate_network_and_subnet(ip_address, network_input, ip_version='ipv4'):
    try:
        if ip_version == 'ipv4':
            ip_network = ipaddress.IPv4Network
            ip_interface = ipaddress.IPv4Interface
            ip_address_class = ipaddress.IPv4Address
        else:
            ip_network = ipaddress.IPv6Network
            ip_interface = ipaddress.IPv6Interface
            ip_address_class = ipaddress.IPv6Address

        if '/' in network_input:
            # Input is in CIDR format
            network = ip_network(network_input, strict=False)
        elif ip_address:
            # Input is in IP + Netmask format
            ip = ip_interface(f"{ip_address}/{network_input}")
            network = ip.network
        else:
            return {"error": "Invalid network input. IP address is required with netmask."}
        
        # Calculate Wildcard, HostMin, HostMax
        wildcard = str(ip_address_class(int(network.hostmask)))
        host_min = str(network.network_address + 1)
        host_max = str(network.broadcast_address - 1)
        
        return {
            "Network Address": str(network.network_address),
            "CIDR": str(network.prefixlen),
            "Netmask": str(network.netmask),
            "Wildcard": wildcard,
            "HostMin": host_min,
            "HostMax": host_max,
            "Total Hosts": network.num_addresses - 2  # Subtract network and broadcast addresses
        }
    except ValueError:
        return {"error": "Invalid network"}

def validate_regex(pattern, text):
    import re
    try:
        regex = re.compile(pattern)
        matches = regex.findall(text)
        return {"matches": matches}
    except re.error:
        return {"error": "Invalid regex pattern"}