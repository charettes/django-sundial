from __future__ import unicode_literals

from django.conf import settings
import pytz


TIMEZONE_SESSION_KEY = getattr(
    settings, 'GREENWICH_TIMEZONE_SESSION_KEY', '_timezone'
)
TIMEZONE_CHOICES = getattr(
    settings, 'GREENWICH_TIMEZONE_CHOICES', list(zip(pytz.common_timezones, pytz.common_timezones))
)
