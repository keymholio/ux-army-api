from django.http import HttpResponseRedirect
from django.conf import settings

class SecureRequiredMiddleware(object):
    def __init__(self):
        self.enabled = getattr(settings, 'HTTPS_SUPPORT')

    def process_request(self, request):
        if self.enabled and not request.is_secure():
            request_url = request.build_absolute_uri(request.get_full_path())
            secure_url = request_url.replace('http://', 'https://')
            return HttpResponseRedirect(secure_url)
        return None