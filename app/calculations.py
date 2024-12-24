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

def calculate_ipv4_network_and_subnet(ip_address, network_input):
    """
    Calculate network and subnet details for IPv4.

    Args:
        ip_address (str): The IPv4 address.
        network_input (str): The network input in CIDR or Netmask format.

    Returns:
        dict: Dictionary containing network and subnet details or error message.
    """
    try:
        if re.match(r'^\d{1,2}$', network_input) and 0 <= int(network_input) <= 32:
            # Input is in CIDR prefix length format (e.g., "24")
            network = ipaddress.IPv4Network(f"{ip_address}/{network_input}", strict=False)
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', network_input):
            # Input is in netmask format (e.g., "255.255.255.0")
            ip = ipaddress.IPv4Interface(f"{ip_address}/{network_input}")
            network = ip.network
        else:
            return {"error": "Invalid network input. Please enter a valid CIDR or Netmask."}
        
        # Calculate Wildcard, HostMin, HostMax
        wildcard = str(ipaddress.IPv4Address(int(network.hostmask)))
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

def calculate_ipv6_network_and_subnet(ip_address, network_input):
    """
    Calculate network and subnet details for IPv6.

    Args:
        ip_address (str): The IPv6 address.
        network_input (str): The network input in CIDR or Netmask format.

    Returns:
        dict: Dictionary containing network and subnet details or error message.
    """
    try:
        if re.match(r'^\d{1,3}$', network_input) and 0 <= int(network_input) <= 128:
            # Input is in CIDR prefix length format (e.g., "64")
            network = ipaddress.IPv6Network(f"{ip_address}/{network_input}", strict=False)
        elif ':' in network_input:
            # Input is in netmask format (e.g., "ffff:ffff:ffff:ffff::")
            ip = ipaddress.IPv6Interface(f"{ip_address}/{network_input}")
            network = ip.network
        else:
            return {"error": "Invalid network input. Please enter a valid CIDR or Netmask."}
        
        # Calculate HostMin, HostMax
        host_min = str(network.network_address + 1)
        host_max = str(network.broadcast_address - 1)
        
        return {
            "Network Address": str(network.network_address),
            "CIDR": str(network.prefixlen),
            "Netmask": str(network.netmask),
            "HostMin": host_min,
            "HostMax": host_max,
            "Total Hosts": network.num_addresses  # No need to subtract for IPv6
        }
    except ValueError:
        return {"error": "Invalid network"}