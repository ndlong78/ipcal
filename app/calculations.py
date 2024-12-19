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

def calculate_network_and_subnet(network_input):
    try:
        if '/' in network_input:
            # Assume input is in CIDR format
            network = ipaddress.ip_network(network_input, strict=False)
            return {
                "Network Address": str(network.network_address),
                "CIDR": str(network.prefixlen),
                "Netmask": str(network.netmask),
                "Total Hosts": network.num_addresses
            }
        else:
            # Assume input is in Netmask format
            cidr = netmask_to_cidr(network_input)
            if cidr:
                network = ipaddress.ip_network('0.0.0.0/' + cidr, strict=False)
                return {
                    "Network Address": str(network.network_address),
                    "CIDR": str(network.prefixlen),
                    "Netmask": network_input,
                    "Total Hosts": network.num_addresses
                }
            else:
                return {"error": "Invalid network"}
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
