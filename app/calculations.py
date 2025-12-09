import ipaddress
import re


def calculate_ipv4(ip_address):
    """Calculate IPv4 address details."""

    try:
        ip = ipaddress.IPv4Address(ip_address)
    except ipaddress.AddressValueError:
        return {"error": "Invalid IPv4 address"}

    return {
        "Address": str(ip),
        "Version": "IPv4",
        "Is Private": ip.is_private,
        "Is Global": ip.is_global,
        "Compressed": ip.exploded,
    }


def calculate_ipv6(ip_address):
    """Calculate IPv6 address details."""

    try:
        ip = ipaddress.IPv6Address(ip_address)
    except ipaddress.AddressValueError:
        return {"error": "Invalid IPv6 address"}

    return {
        "Address": str(ip),
        "Version": "IPv6",
        "Is Private": ip.is_private,
        "Is Global": ip.is_global,
        "Compressed": ip.compressed,
        "Exploded": ip.exploded,
    }


def calculate_ipv4_network_and_subnet(ip_address, network_input):
    """Calculate network and subnet details for IPv4."""

    try:
        if re.match(r"^\d{1,2}$", network_input) and 0 <= int(network_input) <= 32:
            network = ipaddress.IPv4Network(f"{ip_address}/{network_input}", strict=False)
        elif re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", network_input):
            ip = ipaddress.IPv4Interface(f"{ip_address}/{network_input}")
            network = ip.network
        else:
            return {"error": "Invalid network input. Please enter a valid CIDR or Netmask."}

        wildcard = str(ipaddress.IPv4Address(int(network.hostmask)))

        total_addresses = network.num_addresses
        if network.prefixlen == 32:
            host_min = host_max = str(network.network_address)
            usable_hosts = 1
        elif network.prefixlen == 31:
            host_min = str(network.network_address)
            host_max = str(network.broadcast_address)
            usable_hosts = 2
        else:
            host_min = str(network.network_address + 1)
            host_max = str(network.broadcast_address - 1)
            usable_hosts = max(total_addresses - 2, 0)

        return {
            "Network Address": str(network.network_address),
            "CIDR": str(network.prefixlen),
            "Netmask": str(network.netmask),
            "Wildcard": wildcard,
            "HostMin": host_min,
            "HostMax": host_max,
            "Total Hosts": usable_hosts,
        }
    except ValueError:
        return {"error": "Invalid network"}


def calculate_ipv6_network_and_subnet(ip_address, network_input):
    """Calculate network and subnet details for IPv6."""

    try:
        if re.match(r"^\d{1,3}$", network_input) and 0 <= int(network_input) <= 128:
            network = ipaddress.IPv6Network(f"{ip_address}/{network_input}", strict=False)
        elif ":" in network_input:
            ip = ipaddress.IPv6Interface(f"{ip_address}/{network_input}")
            network = ip.network
        else:
            return {"error": "Invalid network input. Please enter a valid CIDR or Netmask."}

        total_addresses = network.num_addresses
        if total_addresses == 1:
            host_min = host_max = str(network.network_address)
        elif network.prefixlen == 127:
            host_min = str(network.network_address)
            host_max = str(network.broadcast_address)
        else:
            host_min = str(network.network_address + 1)
            host_max = str(network.broadcast_address - 1)

        return {
            "Network Address": str(network.network_address),
            "CIDR": str(network.prefixlen),
            "Netmask": str(network.netmask),
            "HostMin": host_min,
            "HostMax": host_max,
            "Total Hosts": network.num_addresses,
        }
    except ValueError:
        return {"error": "Invalid network"}
