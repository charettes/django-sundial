from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
import pytz

from sundial.forms import TimezoneField, TimezoneChoiceField
from sundial.zones import ALL_CHOICES

from .forms import TimezoneFieldModelForm, TimezoneChoiceFieldModelForm


default_timezone = pytz.timezone(settings.TIME_ZONE)


class TimezoneFieldTests(TestCase):
    def test_coercing(self):
        field = TimezoneField()
        self.assertEqual(
            field.clean(settings.TIME_ZONE),
            pytz.timezone(settings.TIME_ZONE)
        )

    def test_empty_values(self):
        field = TimezoneField(required=False)
        self.assertEqual(field.clean(''), '')
        self.assertEqual(field.clean(None), '')

    def test_invalid_value(self):
        field = TimezoneField()
        self.assertRaises(ValidationError, field.clean, 'invalid')

    def test_modelform(self):
        form = TimezoneFieldModelForm({'timezone': settings.TIME_ZONE})
        self.assertTrue(form.is_valid())


class TimezoneChoiceFieldTests(TestCase):
    def test_coercing(self):
        field = TimezoneChoiceField(choices=ALL_CHOICES)
        self.assertEqual(
            field.clean(settings.TIME_ZONE),
            pytz.timezone(settings.TIME_ZONE)
        )

    def test_empty_values(self):
        field = TimezoneChoiceField(choices=ALL_CHOICES, required=False)
        self.assertEqual(field.clean(''), '')
        self.assertEqual(field.clean(None), '')

    def test_invalid_value(self):
        field = TimezoneChoiceField(choices=ALL_CHOICES)
        self.assertRaises(ValidationError, field.clean, 'invalid')

    def test_modelform(self):
        form = TimezoneChoiceFieldModelForm({'choices_timezone': settings.TIME_ZONE})
        self.assertTrue(form.is_valid())
