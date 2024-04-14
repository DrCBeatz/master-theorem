from django.http import HttpResponseForbidden
from django.conf import settings

class ELBHealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # All all requests from the ELB Health Checker
        if 'ELB-HealthChecker/2.0' in request.META.get('HTTP_USER_AGENT', ''):
            return self.get_response(request)
        # Validate against ALLOWED_HOSTS
        host = request.get_host().split(':')[0]
        if host not in settings.ALLOWED_HOSTS:
            return HttpResponseForbidden('Host not allowed')
        return self.get_response(request)