from __future__ import unicode_literals

import django
import pytz
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.functional import cached_property

from . import forms
from .utils import coerce_timezone
from .zones import TimezoneChoices


class TimezoneField(models.CharField):
    default_max_length = 42

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', self.default_max_length)
        super(TimezoneField, self).__init__(*args, **kwargs)

    def _from_db_value(self, value, expression, connection):
        if value:
            value = coerce_timezone(value)
        return value

    if django.VERSION >= (2, 0):
        from_db_value = _from_db_value
    else:
        def from_db_value(self, value, expression, connection, context):
            return self._from_db_value(value, expression, connection)

    def to_python(self, value):
        value = super(TimezoneField, self).to_python(value)
        if value:
            value = coerce_timezone(value)
        return value

    def validate(self, value, model_instance):
        super(TimezoneField, self).validate(force_text(value), model_instance)

    def run_validators(self, value):
        super(TimezoneField, self).run_validators(force_text(value))

    def get_prep_value(self, value):
        if value is not None:
            value = force_text(value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(TimezoneField, self).deconstruct()
        if kwargs.get('max_length') == self.default_max_length:
            del kwargs['max_length']
        choices = self.choices
        if isinstance(choices, TimezoneChoices):
            kwargs['choices'] = choices
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', forms.TimezoneField)
        kwargs.setdefault('choices_form_class', forms.TimezoneChoiceField)
        return super(TimezoneField, self).formfield(**kwargs)


class DateTimeField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        self.db_timezone = kwargs.pop('db_timezone', settings.TIME_ZONE) or 'UTC'
        super(DateTimeField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DateTimeField, self).deconstruct()
        kwargs['db_timezone'] = self.db_timezone
        return name, path, args, kwargs

    @cached_property
    def db_tzinfo(self):
        return pytz.timezone(self.db_timezone)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None or hasattr(value, 'resolve_expression'):
            return value

        if (settings.USE_TZ and
                not connection.features.supports_timezones and timezone.is_aware(value)):
            return timezone.make_naive(value, self.db_tzinfo)

        return super(DateTimeField, self).get_db_prep_value(value, connection, prepared)

    def _from_db_value(self, value, expression, connection):
        if value is None:
            return value

        if settings.USE_TZ and not connection.features.supports_timezones:
            # At this point the value will be in UTC even if the actual field's
            # timezone is self.db_timezone. Replace the bogus timezone with the
            # appropriate one and convert back to the expected UTC.
            value = timezone.make_aware(
                value.replace(tzinfo=None), self.db_tzinfo
            ).astimezone(timezone.utc)

        return value

    if django.VERSION >= (2, 0):
        from_db_value = _from_db_value
    else:
        def from_db_value(self, value, expression, connection, context=None):
            return self._from_db_value(value, expression, connection)
