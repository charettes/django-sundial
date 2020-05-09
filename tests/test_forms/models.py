from django.conf import settings
from django.db import models

from sundial.fields import TimezoneField
from sundial.zones import ALL_GROUPED_CHOICES


class TimezoneModel(models.Model):
    timezone = TimezoneField(default=settings.TIME_ZONE)
    choices_timezone = TimezoneField(blank=True, choices=ALL_GROUPED_CHOICES)
