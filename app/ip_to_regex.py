import ipaddress
from typing import List


def ip_to_regex(ip_cidr: str) -> List[str]:
    """Return a list of CIDR blocks that cover the provided network.

    The previous implementation attempted to build a regular expression for the
    IP range by interpolating start and end octets/hextets directly into a
    pattern. That approach produced invalid expressions such as ``(10-200)``
    which match the literal string ``"10-200"`` instead of the intended numeric
    interval. In order to provide reliable information to the caller, we
    summarise the network into the minimal set of CIDR blocks.

    Args:
        ip_cidr: IP address with subnet mask, e.g. ``"172.30.151.224/27"`` or
            ``"2001:0db8:85a3::/64"``.

    Returns:
        A list of strings representing CIDR blocks that exactly cover the
        supplied network.
    """

    network = ipaddress.ip_network(ip_cidr, strict=False)
    summary = ipaddress.summarize_address_range(
        network.network_address, network.broadcast_address
    )
    return [str(net) for net in summary]
