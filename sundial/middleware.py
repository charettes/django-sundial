from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .utils import get_session_timezone


class TimezoneMiddleware(MiddlewareMixin):
    """Middleware that sets the current timezone from a session stored value.

    Use ``sundial.utils.set_session_timezone()`` to store a user based value
    by registering a receiver on the ``django.contrib.auth.signals.user_logged_in``
    signal or override the ``get_timezone_from_request()`` method in a subclass
    to provide your own mechanism (e.g. GEOIP based)
    """

    def get_timezone_from_request(self, request):
        session = getattr(request, 'session', None)
        if session:
            return get_session_timezone(session)

    def process_request(self, request):
        zone = self.get_timezone_from_request(request)
        if zone:
            timezone.activate(zone)
