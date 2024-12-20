import ipaddress

def calculate_ipv4(ip_address):
    # Example logic for calculating IPv4 details
    ip_info = {
        'IP Address': ip_address,
        'Is Private': ipaddress.ip_address(ip_address).is_private,
        'Is Global': not ipaddress.ip_address(ip_address).is_private
    }
    return ip_info

def calculate_network_and_subnet(ip_address, network_input):
    # Example logic for calculating network and subnet details
    network = ipaddress.ip_network(network_input, strict=False)
    
    # Calculate Wildcard, HostMin, HostMax
    wildcard = str(ipaddress.IPv4Address(int(network.hostmask)))
    host_min = str(network.network_address + 1)
    host_max = str(network.broadcast_address - 1)
    
    network_info = {
        'Network Address': str(network.network_address),
        'CIDR': network.prefixlen,
        'Netmask': str(network.netmask),
        'Wildcard': wildcard,
        'HostMin': host_min,
        'HostMax': host_max,
        'Total Hosts': network.num_addresses - 2  # Subtract network and broadcast addresses
    }
    return network_info