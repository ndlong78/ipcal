import logging
import re
import ipaddress
from flask import Blueprint, render_template, request, flash

from .calculations import (
    calculate_ipv4,
    calculate_ipv6,
    calculate_ipv4_network_and_subnet,
    calculate_ipv6_network_and_subnet,
)
from .ip_to_regex import ip_to_regex

logging.basicConfig(level=logging.DEBUG)

main_bp = Blueprint('main', __name__)

ALLOWED_INPUT_PATTERN = re.compile(r'^[0-9a-fA-F:./]+$')
_IPV4_NETMASK_REGEX = re.compile(r'^(25[0-5]|2[0-4]\d|1?\d?\d)(\.(25[0-5]|2[0-4]\d|1?\d?\d)){3}$')


def validate_raw_input(value, field_name):
    if value is None or value == '':
        raise ValueError(f"{field_name} is required.")
    if not ALLOWED_INPUT_PATTERN.fullmatch(value):
        raise ValueError(
            f"{field_name} contains invalid characters. Only digits, a-f, A-F, ':', '.', '/' are allowed."
        )
    return value


def validate_network_input(network_input, ip_version):
    if ip_version == 4:
        if re.fullmatch(r'\d{1,2}', network_input):
            prefix = int(network_input)
            if not 0 <= prefix <= 32:
                raise ValueError("CIDR prefix length for IPv4 must be between 0 and 32.")
            return

        if _IPV4_NETMASK_REGEX.fullmatch(network_input):
            try:
                ipaddress.IPv4Network(f"0.0.0.0/{network_input}", strict=False)
            except ValueError as exc:
                raise ValueError(f"IPv4 netmask is not valid: {exc}") from exc
            return

        raise ValueError("IPv4 network input must be a CIDR prefix (0-32) or netmask with octets between 0 and 255.")

    if re.fullmatch(r'\d{1,3}', network_input):
        prefix = int(network_input)
        if not 0 <= prefix <= 128:
            raise ValueError("CIDR prefix length for IPv6 must be between 0 and 128.")
        return

    if ':' in network_input:
        try:
            ipaddress.IPv6Network(f"::/{network_input}", strict=False)
        except ValueError as exc:
            raise ValueError(f"IPv6 netmask is not valid: {exc}") from exc
        return

    raise ValueError("IPv6 network input must be a CIDR prefix (0-128) or a valid IPv6 netmask.")


@main_bp.route('/')
def index():
    """Render the main index page."""
    return render_template('index.html')


@main_bp.route('/calculate', methods=['POST'])
def calculate():
    """Handle the calculation of IP details and network details."""
    result = {}

    try:
        ip_address = validate_raw_input(request.form.get('ip-address'), 'IP address')
        network_input = validate_raw_input(request.form.get('network'), 'Network input')

        try:
            ip = ipaddress.ip_address(ip_address)
        except ValueError as exc:
            raise ValueError("Invalid IP address format.") from exc

        validate_network_input(network_input, ip.version)

        if ip.version == 4:
            ip_result = calculate_ipv4(ip_address)
            network_result = calculate_ipv4_network_and_subnet(ip_address, network_input)
        else:
            ip_result = calculate_ipv6(ip_address)
            network_result = calculate_ipv6_network_and_subnet(ip_address, network_input)

        if 'error' in network_result:
            flash(network_result['error'], 'error')
            return render_template('index.html')

        result['ip'] = ip_result
        result['network'] = network_result

        cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
        regex_pattern = ip_to_regex(cidr)
        result['regex'] = {"pattern": regex_pattern}
    except ValueError as exc:
        flash(str(exc), 'error')
        return render_template('index.html')

    return render_template('index.html', result=result)
