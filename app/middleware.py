from .models import Stats
from django.db.models import F
from django.core.cache import cache


class DemoMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]  # Recieves the real ip for each user
        else:  # If x_forwarded for is none, means the request comes directly from user to django server
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def stats(self, os_info):
        os_info = os_info.lower()
        if "windows" in os_info:
            Stats.objects.all().update(win=F("win") + 1)
        elif "mac" in os_info:
            Stats.objects.all().update(mac=F("mac") + 1)
        elif "iphone" in os_info:
            Stats.objects.all().update(iphone=F("iphone") + 1)
        elif "android" in os_info:
            Stats.objects.all().update(android=F("android") + 1)
        else:
            Stats.objects.all().update(other=F("other") + 1)

    def __call__(self, request):
        accept_header = request.META.get("HTTP_ACCEPT", "")
        if "text/html" not in accept_header:
            return self.get_response(request)
        ip = self.get_client_ip(request)
        cache_key = f"os_stats_limit_{ip}"
        if not cache.get(cache_key):
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            self.stats(user_agent)
            cache.set(cache_key, True, 300)

        response = self.get_response(request)
        return response
