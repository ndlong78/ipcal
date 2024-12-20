import re
import ipaddress

def ip_to_regex(ip_cidr):
    """
    Convert IP address and subnet mask (CIDR) to a regular expression (regex).

    Args:
        ip_cidr (str): IP address with subnet mask, e.g., "172.30.135.192/26".

    Returns:
        str: Regex matching the IP range.
    """
    network = ipaddress.ip_network(ip_cidr, strict=False)
    first_ip = int(network.network_address)
    last_ip = int(network.broadcast_address)

    def ip_to_octets(ip):
        return [(ip >> 24) & 0xFF, (ip >> 16) & 0xFF, (ip >> 8) & 0xFF, ip & 0xFF]

    start_octets = ip_to_octets(first_ip)
    end_octets = ip_to_octets(last_ip)

    regex_parts = []
    for i in range(4):
        if start_octets[i] == end_octets[i]:
            regex_parts.append(f"{start_octets[i]}")
        else:
            regex_parts.append(f"({start_octets[i]}-{end_octets[i]})")

    # Use string join without f-strings for the literal backslash
    return "^" + r"\.".join(regex_parts) + "$"

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