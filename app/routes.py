import logging
import warnings
from flask import Blueprint, render_template, request, flash
import re
from .calculations import calculate_ipv4, calculate_ipv6, calculate_network_and_subnet
from .ip_to_regex import ip_to_regex, validate_regex

# Thiết lập logging
logging.basicConfig(level=logging.DEBUG)

main_bp = Blueprint('main', __name__)

def filter_ip_input(ip_input):
    # Regular expression to match valid IP address characters
    valid_ip_pattern = re.compile(r'[^0-9a-fA-F:./]')
    # Remove invalid characters
    filtered_ip = re.sub(valid_ip_pattern, '', ip_input)
    logging.debug(f"Filtered IP input: {filtered_ip}")
    return filtered_ip

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    result = {}

    ip_type = request.form.get('ip-type')
    ip_address = filter_ip_input(request.form.get('ip-address'))
    network_input = filter_ip_input(request.form.get('network'))

    logging.debug(f"IP type: {ip_type}, IP address: {ip_address}, Network input: {network_input}")

    if not network_input:
        error_message = "Network input is required."
        warnings.warn(error_message)
        flash(error_message, 'error')
        return render_template('index.html')

    if ip_type == 'ipv4':
        if ip_address:
            ipv4_result = calculate_ipv4(ip_address)
            if 'error' in ipv4_result:
                warnings.warn(f"Invalid IPv4 address: {ip_address}")
            result['ip'] = ipv4_result
        network_result = calculate_network_and_subnet(ip_address, network_input, ip_version='ipv4')
        if 'error' in network_result:
            warnings.warn(f"Invalid network input for IPv4: {network_input}")
        result['network'] = network_result
        if 'error' not in network_result:
            cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
            regex_pattern = ip_to_regex(cidr)
            result['regex'] = {"pattern": regex_pattern}

    elif ip_type == 'ipv6':
        if ip_address:
            ipv6_result = calculate_ipv6(ip_address)
            if 'error' in ipv6_result:
                warnings.warn(f"Invalid IPv6 address: {ip_address}")
            result['ip'] = ipv6_result
        network_result = calculate_network_and_subnet(ip_address, network_input, ip_version='ipv6')
        if 'error' in network_result:
            warnings.warn(f"Invalid network input for IPv6: {network_input}")
        result['network'] = network_result
        if 'error' not in network_result:
            cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
            regex_pattern = ip_to_regex(cidr)
            result['regex'] = {"pattern": regex_pattern}

    return render_template('index.html', result=result)