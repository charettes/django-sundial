from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import force_text

from . import forms
from .utils import coerce_timezone
from .zones import TimezoneChoices


class TimezoneField(models.CharField):
    default_max_length = 42

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', self.default_max_length)
        super(TimezoneField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if value:
            value = coerce_timezone(value)
        return value

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
