from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
import pytz

from sundial.forms import TimezoneField

default_timezone = pytz.timezone(settings.TIME_ZONE)


class TimezoneFieldTests(TestCase):
    def test_coercing(self):
        field = TimezoneField()
        self.assertEqual(
            field.clean(settings.TIME_ZONE),
            pytz.timezone(settings.TIME_ZONE)
        )

    def test_invalid_value(self):
        field = TimezoneField()
        self.assertRaises(ValidationError, field.clean, 'invalid')
