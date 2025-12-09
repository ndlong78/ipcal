import ipaddress
import re


def calculate_ipv4(ip_address):
    """Return IPv4 address details."""
    ip = ipaddress.IPv4Address(ip_address)
    return {
        "Address": str(ip),
        "Version": "IPv4",
        "Binary": bin(int(ip))[2:].zfill(32),
        "Hexadecimal": hex(int(ip))[2:],
        "Is Private": ip.is_private,
        "Reverse Pointer": ip.reverse_pointer,
    }


def calculate_ipv6(ip_address):
    """Return IPv6 address details."""
    ip = ipaddress.IPv6Address(ip_address)
    return {
        "Address": str(ip),
        "Version": "IPv6",
        "Binary": bin(int(ip))[2:].zfill(128),
        "Hexadecimal": hex(int(ip))[2:],
        "Is Private": ip.is_private,
        "Reverse Pointer": ip.reverse_pointer,
    }


def _ipv4_netmask_regex():
    octet = r"(25[0-5]|2[0-4]\d|1?\d?\d)"
    return rf"^{octet}(\.{octet}){{3}}$"


def calculate_ipv4_network_and_subnet(ip_address, network_input):
    """Calculate IPv4 network details from CIDR prefix or netmask."""
    try:
        if re.fullmatch(r"\d{1,2}", network_input):
            network = ipaddress.IPv4Network(f"{ip_address}/{network_input}", strict=False)
        elif re.fullmatch(_ipv4_netmask_regex(), network_input):
            interface = ipaddress.IPv4Interface(f"{ip_address}/{network_input}")
            network = interface.network
        else:
            return {"error": "Network input must be a CIDR prefix (0-32) or IPv4 netmask."}

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
    except ValueError as exc:
        return {"error": f"Invalid IPv4 network: {exc}"}


def calculate_ipv6_network_and_subnet(ip_address, network_input):
    """Calculate IPv6 network details from CIDR prefix or netmask."""
    try:
        if re.fullmatch(r"\d{1,3}", network_input):
            network = ipaddress.IPv6Network(f"{ip_address}/{network_input}", strict=False)
        elif ":" in network_input:
            interface = ipaddress.IPv6Interface(f"{ip_address}/{network_input}")
            network = interface.network
        else:
            return {"error": "Network input must be a CIDR prefix (0-128) or IPv6 netmask."}

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
            "Total Hosts": total_addresses,
        }
    except ValueError as exc:
        return {"error": f"Invalid IPv6 network: {exc}"}
