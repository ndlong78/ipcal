import logging
import re
import ipaddress
import secrets
import time
from flask import Blueprint, render_template, request, flash, session, current_app

from .calculations import (
    calculate_ipv4,
    calculate_ipv6,
    calculate_ipv4_network_and_subnet,
    calculate_ipv6_network_and_subnet,
)
from .ip_to_regex import ip_to_regex

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)
CSRF_SESSION_KEY = "csrf_token"
RATE_LIMIT_WINDOW_SECONDS = 60
_rate_limit_cache: dict[str, list[float]] = {}


def filter_ip_input(ip_input: str, allow_slash: bool = True) -> str:
    """Remove invalid characters from the IP input."""
    pattern = r"[^0-9a-fA-F:./]" if allow_slash else r"[^0-9a-fA-F:.]"
    valid_ip_pattern = re.compile(pattern)
    filtered_ip = re.sub(valid_ip_pattern, "", ip_input)
    logger.debug("Filtered IP input: %s", filtered_ip)
    return filtered_ip


def is_valid_cidr_or_netmask(network_input, ip_version="ipv4"):
    """Check if the network input is a valid CIDR or Netmask."""
    try:
        if ip_version == "ipv4":
            if re.match(r"^\d{1,2}$", network_input) and 0 <= int(network_input) <= 32:
                logger.debug("Valid CIDR prefix length: %s", network_input)
                return True
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", network_input):
                ipaddress.IPv4Network(f"0.0.0.0/{network_input}", strict=False)
                logger.debug("Valid Netmask: %s", network_input)
                return True
        else:
            if re.match(r"^\d{1,3}$", network_input) and 0 <= int(network_input) <= 128:
                logger.debug("Valid CIDR prefix length: %s", network_input)
                return True
            if ":" in network_input:
                ipaddress.IPv6Network(f"::/{network_input}", strict=False)
                logger.debug("Valid Netmask: %s", network_input)
                return True
    except ValueError:
        logger.debug("Invalid CIDR or Netmask: %s", network_input)

    return False


def get_or_set_csrf_token() -> str:
    """Ensure CSRF token exists in session."""
    token = session.get(CSRF_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
    return token


def validate_csrf_token(form_token: str | None) -> None:
    """Validate CSRF token from form submission."""
    session_token = session.get(CSRF_SESSION_KEY)
    if not form_token or not session_token or form_token != session_token:
        raise ValueError("Invalid CSRF token.")


def is_rate_limited(remote_addr: str, limit: int) -> bool:
    """Simple in-memory rate limiter per IP."""
    now = time.time()
    timestamps = _rate_limit_cache.get(remote_addr, [])
    timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW_SECONDS]
    if len(timestamps) >= limit:
        _rate_limit_cache[remote_addr] = timestamps
        return True
    timestamps.append(now)
    _rate_limit_cache[remote_addr] = timestamps
    return False


def validate_raw_input(value: str | None, field_name: str, allow_slash: bool = False) -> str:
    """Validate raw input for required fields and invalid characters."""
    if value is None or not value.strip():
        raise ValueError(f"{field_name} is required.")
    value = value.strip()
    filtered_value = filter_ip_input(value, allow_slash=allow_slash)
    if filtered_value != value:
        raise ValueError(f"{field_name} contains invalid characters.")
    return value


def validate_network_input(network_input: str, ip_version: int) -> None:
    """Validate network input based on IP version."""
    if ip_version == 4:
        if re.match(r"^\d{1,2}$", network_input):
            cidr = int(network_input)
            if not 0 <= cidr <= 32:
                raise ValueError("CIDR prefix length must be between 0 and 32.")
            return
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", network_input):
            octets = network_input.split(".")
            if any(int(octet) > 255 for octet in octets):
                raise ValueError("Netmask must contain octets between 0 and 255.")
            try:
                ipaddress.IPv4Network(f"0.0.0.0/{network_input}", strict=False)
            except ValueError as exc:
                raise ValueError("Invalid IPv4 netmask format.") from exc
            return
        raise ValueError("Invalid network input. Please enter a valid CIDR or Netmask.")

    if re.match(r"^\d{1,3}$", network_input):
        cidr = int(network_input)
        if not 0 <= cidr <= 128:
            raise ValueError("CIDR prefix length must be between 0 and 128.")
        return
    if ":" in network_input:
        try:
            ipaddress.IPv6Network(f"::/{network_input}", strict=False)
        except ValueError as exc:
            raise ValueError("Invalid IPv6 netmask format.") from exc
        return

    raise ValueError("Invalid network input. Please enter a valid CIDR or Netmask.")


def render_index(result: dict | None = None):
    """Render the main index page with CSRF token."""
    csrf_token = get_or_set_csrf_token()
    return render_template("index.html", result=result, csrf_token=csrf_token)


@main_bp.route('/')
def index():
    """Render the main index page."""
    return render_index()


@main_bp.route('/calculate', methods=['POST'])
def calculate():
    """Handle the calculation of IP details and network details."""
    result = {}

    try:
        if not current_app.config.get("RATE_LIMIT_DISABLED", False):
            limit = current_app.config.get("RATE_LIMIT_PER_MINUTE", 60)
            remote_addr = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")
            if is_rate_limited(remote_addr, limit):
                flash("Too many requests. Please try again later.", "error")
                return render_index()

        validate_csrf_token(request.form.get("csrf_token"))

        ip_address = validate_raw_input(request.form.get("ip-address"), "IP address")
        network_input = validate_raw_input(
            request.form.get("network"),
            "Network input",
            allow_slash=True,
        )

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

        if "error" in network_result:
            flash(network_result["error"], "error")
            return render_index()

        result["ip"] = ip_result
        result["network"] = network_result

        cidr = f"{network_result['Network Address']}/{network_result['CIDR']}"
        regex_pattern = ip_to_regex(cidr)
        result["regex"] = {"pattern": regex_pattern}
    except ValueError as exc:
        flash(str(exc), "error")
        return render_index()

    return render_index(result=result)
