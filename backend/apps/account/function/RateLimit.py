from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled

class RateLimit(SimpleRateThrottle):
    scope ='otp'
    def get_cache_key(self, request, view):
        phone = request.data.get("phone")
        if not phone :
            return None
        return self.cache_format%{
            "scope":self.scope,
            "ident":phone,
        }
    def throttle_failure(self):
        wait = self.wait()
        raise Throttled(
            detail=f"Too many OTP requests .Try again after {int(wait)} seconds.",
            wait =wait
        )
        