import ipaddress
import re

def ip_to_regex(ip_cidr):
    """
    Convert IP address and subnet mask (CIDR) to a regular expression (regex).

    Args:
        ip_cidr (str): IP address with subnet mask, e.g., "192.168.1.0/29".

    Returns:
        str: Regex matching the IP range.
    """
    network = ipaddress.ip_network(ip_cidr, strict=False)
    first_ip = int(network.network_address)
    last_ip = int(network.broadcast_address)

    def ip_to_regex_range(start, end):
        """Create regex for an IP address range."""
        def to_regex(octet_start, octet_end):
            if octet_start == octet_end:
                return str(octet_start)
            return f"{octet_start}-{octet_end}"

        ranges = []
        for i in range(4):
            start_octet = (start >> (8 * (3 - i))) & 0xFF
            end_octet = (end >> (8 * (3 - i))) & 0xFF
            ranges.append(to_regex(start_octet, end_octet))

        return "^" + r"\.".join(ranges) + "$"

    return ip_to_regex_range(first_ip, last_ip)

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
