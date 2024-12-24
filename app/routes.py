import logging
import warnings
from flask import Blueprint, render_template, request, flash
import re
import ipaddress
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

def is_valid_cidr_or_netmask(network_input):
    try:
        # Kiểm tra nếu là CIDR
        ipaddress.ip_network(network_input, strict=False)
        return True
    except ValueError:
        # Kiểm tra nếu là Netmask
        parts = network_input.split()
        if len(parts) == 2:
            ip, netmask = parts
            try:
                ipaddress.ip_address(ip)
                ipaddress.IPv4Network(f"0.0.0.0/{netmask}", strict=False)
                return True
            except ValueError:
                pass
    return False

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    result = {}

    ip_address = filter_ip_input(request.form.get('ip-address'))
    network_input = filter_ip_input(request.form.get('network'))

    logging.debug(f"IP address: {ip_address}, Network input: {network_input}")

    if not network_input or not is_valid_cidr_or_netmask(network_input):
        error_message = "Invalid network input. Please enter a valid CIDR or IP + Netmask."
        warnings.warn(error_message)
        flash(error_message, 'error')
        return render_template('index.html')

    try:
        ip = ipaddress.ip_address(ip_address)
        if ip.version == 4:
            ip_result = calculate_ipv4(ip_address)
            network_result = calculate_network_and_subnet(ip_address, network_input, ip_version='ipv4')
        else:
            ip_result = calculate_ipv6(ip_address)
            network_result = calculate_network_and_subnet(ip_address, network_input, ip_version='ipv6')

        if 'error' in network_result:
            warnings.warn(f"Invalid network input: {network_input}")
        
        result['ip'] = ip_result
        result['network'] = network_result

        if 'error' not in network_result:
            cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
            regex_pattern = ip_to_regex(cidr)
            result['regex'] = {"pattern": regex_pattern}
    except ValueError:
        error_message = "Invalid IP address."
        warnings.warn(error_message)
        flash(error_message, 'error')
        return render_template('index.html')

    return render_template('index.html', result=result)