from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from sundial.fields import DateTimeField, TimezoneField


class TimezoneModel(models.Model):
    timezone = TimezoneField(default=settings.TIME_ZONE)
    blank_timezone = TimezoneField(blank=True)
    null_timezone = TimezoneField(blank=True, null=True)


@python_2_unicode_compatible
class DbTimezoneModel(models.Model):
    datetime = DateTimeField(db_timezone='Europe/Amsterdam')

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return models.Model.__str__(self)
