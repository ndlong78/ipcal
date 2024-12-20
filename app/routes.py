from flask import Blueprint, render_template, request
import re
from .calculations import calculate_ipv4, calculate_network_and_subnet
from .ip_to_regex import ip_to_regex, validate_regex

main_bp = Blueprint('main', __name__)

def filter_ip_input(ip_input):
    # Regular expression to match valid IP address characters
    valid_ip_pattern = re.compile(r'[^0-9./]')
    # Remove invalid characters
    filtered_ip = re.sub(valid_ip_pattern, '', ip_input)
    return filtered_ip

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    result = {}

    ipv4_address = filter_ip_input(request.form.get('ipv4'))
    network_input = filter_ip_input(request.form.get('network'))

    if ipv4_address:
        ipv4_result = calculate_ipv4(ipv4_address)
        result['ipv4'] = ipv4_result

    if network_input:
        network_result = calculate_network_and_subnet(ipv4_address, network_input)
        result['network'] = network_result
        if 'error' not in network_result:
            cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
            regex_pattern = ip_to_regex(cidr)
            result['regex'] = {"pattern": regex_pattern}

    return render_template('index.html', result=result)