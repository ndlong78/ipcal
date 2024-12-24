import re
import ipaddress

def ip_to_regex(ip_cidr):
    """
    Convert IP address and subnet mask (CIDR) to a regular expression (regex).

    Args:
        ip_cidr (str): IP address with subnet mask, e.g., "172.30.151.224/27" or "2001:0db8:85a3::/64".

    Returns:
        str: Regex matching the IP range.
    """
    network = ipaddress.ip_network(ip_cidr, strict=False)
    first_ip = int(network.network_address)
    last_ip = int(network.broadcast_address)

    def ipv4_to_octets(ip):
        return [(ip >> 24) & 0xFF, (ip >> 16) & 0xFF, (ip >> 8) & 0xFF, ip & 0xFF]

    def ipv6_to_hextets(ip):
        return [(ip >> (8 * i)) & 0xFFFF for i in range(7, -1, -1)]

    if network.version == 4:
        start_octets = ipv4_to_octets(first_ip)
        end_octets = ipv4_to_octets(last_ip)

        regex_parts = []
        for i in range(4):
            if start_octets[i] == end_octets[i]:
                regex_parts.append(f"{start_octets[i]}")
            else:
                regex_parts.append(f"({start_octets[i]}-{end_octets[i]})")

        regex_str = "^" + r"\.".join(regex_parts) + "$"
    else:
        start_hextets = ipv6_to_hextets(first_ip)
        end_hextets = ipv6_to_hextets(last_ip)

        regex_parts = []
        for i in range(8):
            if start_hextets[i] == end_hextets[i]:
                regex_parts.append(f"{start_hextets[i]:x}")
            else:
                regex_parts.append(f"({start_hextets[i]:x}-{end_hextets[i]:x})")

        regex_str = "^" + ":".join(regex_parts) + "$"

    return regex_str

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

# Example usage
if __name__ == "__main__":
    ipv4_cidr = "192.168.1.0/24"
    ipv6_cidr = "2001:0db8:85a3::/64"

    ipv4_regex = ip_to_regex(ipv4_cidr)
    ipv6_regex = ip_to_regex(ipv6_cidr)

    print(f"IPv4 CIDR: {ipv4_cidr} -> Regex: {ipv4_regex}")
    print(f"IPv6 CIDR: {ipv6_cidr} -> Regex: {ipv6_regex}")