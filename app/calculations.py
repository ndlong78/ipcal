import ipaddress
import re

def calculate_ipv4(ip_address):
    """
    Calculate details for an IPv4 address.

    Args:
        ip_address (str): The IPv4 address to calculate details for.

    Returns:
        dict: Dictionary containing IP details or error message.
    """
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
    """
    Calculate details for an IPv6 address.

    Args:
        ip_address (str): The IPv6 address to calculate details for.

    Returns:
        dict: Dictionary containing IP details or error message.
    """
    try:
        ip = ipaddress.ip_address(ip_address)
        return {
            "IP Address": str(ip),
            "Is Private": ip.is_private,
            "Is Global": not ip.is_private
        }
    except ValueError:
        return {"error": "Invalid IPv6 address"}

def calculate_network_and_subnet(ip_address, network_input, ip_version='ipv4'):
    """
    Calculate network and subnet details.

    Args:
        ip_address (str): The IP address.
        network_input (str): The network input in CIDR or Netmask format.
        ip_version (str): The version of IP ('ipv4' or 'ipv6').

    Returns:
        dict: Dictionary containing network and subnet details or error message.
    """
    try:
        if ip_version == 'ipv4':
            ip_network = ipaddress.IPv4Network
            ip_interface = ipaddress.IPv4Interface
            ip_address_class = ipaddress.IPv4Address
        else:
            ip_network = ipaddress.IPv6Network
            ip_interface = ipaddress.IPv6Interface
            ip_address_class = ipaddress.IPv6Address

        if re.match(r'^\d{1,2}$', network_input) and 0 <= int(network_input) <= 128:
            # Input is in CIDR prefix length format (e.g., "24" or "64" for IPv6)
            network = ip_network(f"{ip_address}/{network_input}", strict=False)
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', network_input) or (':' in network_input):
            # Input is in netmask format (e.g., "255.255.255.0" for IPv4 or "ffff:ffff:ffff:ffff::" for IPv6)
            ip = ip_interface(f"{ip_address}/{network_input}")
            network = ip.network
        else:
            return {"error": "Invalid network input. Please enter a valid CIDR or Netmask."}
        
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
            "Total Hosts": network.num_addresses - 2 if ip_version == 'ipv4' else network.num_addresses
        }
    except ValueError:
        return {"error": "Invalid network"}