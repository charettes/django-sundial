from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from sundial.middleware import TimezoneMiddleware
from sundial.utils import set_session_timezone


class TimezoneMiddlewareTests(TestCase):
    request_factory = RequestFactory()
    session_middleware = SessionMiddleware()
    middleware = TimezoneMiddleware()

    def tearDown(self):
        timezone.deactivate()

    def test_missing_session(self):
        request = self.request_factory.get('/')
        self.middleware.process_request(request)
        self.assertEqual(timezone.get_current_timezone_name(), settings.TIME_ZONE)

    def test_missing_session_timezone(self):
        request = self.request_factory.get('/')
        self.session_middleware.process_request(request)
        self.middleware.process_request(request)
        self.assertEqual(timezone.get_current_timezone_name(), settings.TIME_ZONE)

    def test_timezone_activation(self):
        request = self.request_factory.get('/')
        self.session_middleware.process_request(request)
        zone = 'America/Montreal'
        set_session_timezone(request.session, zone)
        self.middleware.process_request(request)
        self.assertEqual(timezone.get_current_timezone_name(), zone)
