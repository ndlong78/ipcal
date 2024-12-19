from flask import Blueprint, render_template, request
from .calculations import calculate_ipv4, calculate_network_and_subnet, validate_regex
from .debug import log_request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    log_request(request)
    result = {}

    ipv4_address = request.form.get('ipv4')
    network_input = request.form.get('network')

    if ipv4_address:
        result['ipv4'] = calculate_ipv4(ipv4_address)

    if network_input:
        result['network'] = calculate_network_and_subnet(ipv4_address, network_input)

    if 'regex' in request.form and 'text' in request.form:
        result['regex'] = validate_regex(request.form['regex'], request.form['text'])

    return render_template('index.html', result=result)
