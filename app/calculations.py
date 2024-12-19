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

def calculate_subnet(network):
    try:
        net = ipaddress.ip_network(network, strict=False)
        return {
            "Network Address": str(net.network_address),
            "Subnet Mask": str(net.netmask),
            "Total Hosts": net.num_addresses
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
