import logging
from flask import Blueprint, render_template, request, flash
import re
import ipaddress
from .calculations import calculate_ipv4, calculate_ipv6, calculate_ipv4_network_and_subnet, calculate_ipv6_network_and_subnet
from .ip_to_regex import ip_to_regex

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define the Blueprint before using it
main_bp = Blueprint('main', __name__)

def filter_ip_input(ip_input):
    """Remove invalid characters from the IP input."""
    valid_ip_pattern = re.compile(r'[^0-9a-fA-F:./]')
    filtered_ip = re.sub(valid_ip_pattern, '', ip_input)
    logging.debug(f"Filtered IP input: {filtered_ip}")
    return filtered_ip

def is_valid_cidr_or_netmask(network_input, ip_version='ipv4'):
    """Check if the network input is a valid CIDR or Netmask."""
    try:
        if ip_version == 'ipv4':
            # Check if it is a valid CIDR prefix length (e.g., "24")
            if re.match(r'^\d{1,2}$', network_input) and 0 <= int(network_input) <= 32:
                logging.debug(f"Valid CIDR prefix length: {network_input}")
                return True
            # Check if it is a valid netmask
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', network_input):
                ipaddress.IPv4Network(f"0.0.0.0/{network_input}", strict=False)
                logging.debug(f"Valid Netmask: {network_input}")
                return True
        else:
            # Check if it is a valid CIDR prefix length (e.g., "64")
            if re.match(r'^\d{1,3}$', network_input) and 0 <= int(network_input) <= 128:
                logging.debug(f"Valid CIDR prefix length: {network_input}")
                return True
            # Check if it is a valid netmask
            if ':' in network_input:
                ipaddress.IPv6Network(f"::/{network_input}", strict=False)
                logging.debug(f"Valid Netmask: {network_input}")
                return True
    except ValueError:
        logging.debug(f"Invalid CIDR or Netmask: {network_input}")
    
    return False

@main_bp.route('/')
def index():
    """Render the main index page."""
    return render_template('index.html')

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    """Handle the calculation of IP details and network details."""
    result = {}

    ip_address = filter_ip_input(request.form.get('ip-address'))
    network_input = filter_ip_input(request.form.get('network'))

    logging.debug(f"IP address: {ip_address}, Network input: {network_input}")

    try:
        ip = ipaddress.ip_address(ip_address)
        if ip.version == 4:
            if not is_valid_cidr_or_netmask(network_input, ip_version='ipv4'):
                raise ValueError("Invalid network input")
            ip_result = calculate_ipv4(ip_address)
            network_result = calculate_ipv4_network_and_subnet(ip_address, network_input)
        else:
            if not is_valid_cidr_or_netmask(network_input, ip_version='ipv6'):
                raise ValueError("Invalid network input")
            ip_result = calculate_ipv6(ip_address)
            network_result = calculate_ipv6_network_and_subnet(ip_address, network_input)

        if 'error' in network_result:
            flash(f"Invalid network input: {network_input}", 'error')
            return render_template('index.html')

        result['ip'] = ip_result
        result['network'] = network_result

        if 'error' not in network_result:
            cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
            regex_pattern = ip_to_regex(cidr)
            result['regex'] = {"pattern": regex_pattern}
    except ValueError as e:
        flash(str(e), 'error')
        return render_template('index.html')

    return render_template('index.html', result=result)