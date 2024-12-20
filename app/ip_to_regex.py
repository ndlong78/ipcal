import re

def ip_to_regex(ip_cidr):
    """
    Convert IP address and subnet mask (CIDR) to a regular expression (regex).

    Args:
        ip_cidr (str): IP address with subnet mask, e.g., "172.30.135.192/26".

    Returns:
        str: Regex matching the IP range.
    """
    # Parse the IP address and CIDR
    ip, cidr = ip_cidr.split('/')
    cidr = int(cidr)

    # Convert IP to a list of octets
    octets = list(map(int, ip.split('.')))

    # Determine the number of bits for the host part
    host_bits = 32 - cidr

    # Calculate the number of addresses in the range
    num_addresses = 2 ** host_bits

    # Calculate the start and end addresses
    start_ip = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
    end_ip = start_ip + num_addresses - 1

    # Convert the range of addresses to regex
    def ip_to_octets(ip):
        return [(ip >> 24) & 0xFF, (ip >> 16) & 0xFF, (ip >> 8) & 0xFF, ip & 0xFF]

    start_octets = ip_to_octets(start_ip)
    end_octets = ip_to_octets(end_ip)

    regex_parts = []
    for i in range(4):
        if start_octets[i] == end_octets[i]:
            regex_parts.append(f"{start_octets[i]}")
        else:
            regex_parts.append(f"[{start_octets[i]}-{end_octets[i]}]")

    return f"^{'.'.join(regex_parts)}$"

def validate_regex(pattern, text):
    """
    Validate a regular expression (regex) against a text string.

    Args:
        pattern (str): Regex pattern.
        text (str): Text string to check.

    Returns:
        dict: Validation result, including matched strings or error message.
    """
    try:
        regex = re.compile(pattern)
        matches = regex.findall(text)
        return {"matches": matches}
    except re.error:
        return {"error": "Invalid regex pattern"}
