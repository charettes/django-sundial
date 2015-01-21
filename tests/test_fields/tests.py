from __future__ import unicode_literals

# TODO: Remove when support for Python 2.6 is dropped
import sys
if sys.version_info >= (2, 7):
    from unittest import skipIf, skipUnless
else:
    from django.utils.unittest import skipIf, skipUnless

import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
import pytz

from sundial.fields import TimezoneField

from .models import TimezoneModel

try:
    import south
except ImportError:
    south = None


default_timezone = pytz.timezone(settings.TIME_ZONE)


class TimezoneFieldTests(TestCase):
    def test_default(self):
        TimezoneModel.objects.create()
        obj = TimezoneModel.objects.get()
        self.assertEqual(obj.timezone, default_timezone)
        self.assertEqual(obj.blank_timezone, '')
        self.assertIsNone(obj.null_timezone)

    def test_filtering(self):
        obj = TimezoneModel.objects.create(timezone=default_timezone)
        self.assertEqual(TimezoneModel.objects.get(timezone=default_timezone), obj)

    @skipUnless(django.VERSION >= (1, 7, 0), 'Field deconstruction is only supported on Django >= 1.7.0')
    def test_deconstruct(self):
        field = TimezoneField(name='timezone')
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'timezone')
        self.assertEqual(path, 'sundial.fields.TimezoneField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {})

        default = 'America/Montreal'
        choices = [(default, 'Montreal')]
        field = TimezoneField(name='timezone', choices=choices, max_length=30, default=default)
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'timezone')
        self.assertEqual(path, 'sundial.fields.TimezoneField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'choices': choices, 'max_length': 30, 'default': 'America/Montreal'})

    @skipIf(south is None, 'South is not installed.')
    def test_south_field_triple(self):
        field = TimezoneField()
        path, args, kwargs = field.south_field_triple()
        self.assertEqual(path, 'sundial.fields.TimezoneField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {})

        default = 'America/Montreal'
        field = TimezoneField(max_length=30, default=default)
        path, args, kwargs = field.south_field_triple()
        self.assertEqual(path, 'sundial.fields.TimezoneField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'max_length': repr(30), 'default': repr(default)})

    def test_to_python(self):
        self.assertRaises(ValidationError, TimezoneField().to_python, 'invalid')

    def test_formfield(self):
        field = TimezoneField(default='America/Montreal')
        formfield = field.formfield()
        self.assertEqual(formfield.clean(default_timezone.zone), default_timezone)
        self.assertEqual(formfield.choices, field.choices)
        self.assertEqual(formfield.initial, 'America/Montreal')
