from __future__ import unicode_literals

from django.forms import TypedChoiceField

from .settings import TIMEZONE_CHOICES
from .utils import coerce_timezone


class TimezoneField(TypedChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('coerce', coerce_timezone)
        kwargs.setdefault('choices', TIMEZONE_CHOICES)
        super(TimezoneField, self).__init__(*args, **kwargs)
