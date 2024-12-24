@main_bp.route('/calculate', methods=['POST'])
def calculate():
    result = {}

    ip_address = request.form.get('ip-address')
    network_input = request.form.get('network')

    # Bỏ qua cảnh báo nếu trường không có giá trị
    if not ip_address:
        ip_address = "0.0.0.0" # Giá trị mặc định hoặc xử lý khác
    if not network_input:
        network_input = "0.0.0.0/0" # Giá trị mặc định hoặc xử lý khác

    ip_address = filter_ip_input(ip_address)
    network_input = filter_ip_input(network_input)

    logging.debug(f"IP address: {ip_address}, Network input: {network_input}")

    if not is_valid_cidr_or_netmask(network_input):
        error_message = "Invalid network input. Please enter a valid CIDR or IP + Netmask."
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
            flash(f"Invalid network input: {network_input}", 'error')
            return render_template('index.html')

        result['ip'] = ip_result
        result['network'] = network_result

        if 'error' not in network_result:
            cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
            regex_pattern = ip_to_regex(cidr)
            result['regex'] = {"pattern": regex_pattern}
    except ValueError:
        error_message = "Invalid IP address."
        flash(error_message, 'error')
        return render_template('index.html')

    return render_template('index.html', result=result)