def log_request(request):
    """Log the details of the incoming request."""
    print(f"Request received: {request.form}")