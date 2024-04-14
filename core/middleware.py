from django.http import HttpResponse
from ipaddress import ip_address, ip_network

class ELBHealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the allowed network
        allowed_network = ip_network("172.31.0.0/16")

        # Get the client's IP address from the request
        client_ip = ip_address(request.META.get("REMOTE_ADDR"))

        # Check if the client IP is in the allowed network
        if client_ip in allowed_network:
            # Mark the host as allowed
            request.META['HTTP_HOST'] = request.get_host()

        response = self.get_response(request)
        return response
