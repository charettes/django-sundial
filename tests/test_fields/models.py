from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from sundial.fields import TimezoneField


class TimezoneModel(models.Model):
    timezone = TimezoneField(default=settings.TIME_ZONE)
    blank_timezone = TimezoneField(blank=True)
    null_timezone = TimezoneField(blank=True, null=True)
