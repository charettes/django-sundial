from __future__ import unicode_literals

from django.conf import settings

from .zones import COMMON_GROUPED_CHOICES


__all__ = ['TIMEZONE_SESSION_KEY', 'TIMEZONE_CHOICES']


TIMEZONE_SESSION_KEY = getattr(
    settings, 'SUNDIAL_TIMEZONE_SESSION_KEY', '_timezone'
)

TIMEZONE_CHOICES = getattr(
    settings, 'SUNDIAL_TIMEZONE_CHOICES', COMMON_GROUPED_CHOICES
)
