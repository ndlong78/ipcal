import ipaddress

def calculate_ipv4(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        return {
            "IP Address": str(ip),
            "Is Private": ip.is_private,
            "Is Global": ip.is_global
        }
    except ValueError:
        return {"error": "Invalid IPv4 address"}

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

def calculate_network_and_subnet(ip_address, network_input):
    try:
        if '/' in network_input:
            # Input is in CIDR format
            network = ipaddress.ip_network(network_input, strict=False)
        elif ip_address:
            # Input is in IP + Netmask format
            ip = ipaddress.ip_interface(f"{ip_address}/{network_input}")
            network = ip.network
        else:
            return {"error": "Invalid network input. IP address is required with netmask."}
        return {
            "Network Address": str(network.network_address),
            "CIDR": str(network.prefixlen),
            "Netmask": str(network.netmask),
            "Total Hosts": network.num_addresses
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
