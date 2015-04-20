from __future__ import unicode_literals

from unittest import skipUnless

import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
import pytz

from sundial.fields import TimezoneField
from sundial.zones import COMMON_GROUPED_CHOICES

from .models import TimezoneModel

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

    def test_full_clean(self):
        # Test zone validation.
        obj = TimezoneModel(timezone=default_timezone.zone)
        obj.full_clean()
        # Test tzinfo validation.
        obj = TimezoneModel(timezone=default_timezone)
        obj.full_clean()
        # Test invalid input.
        with self.assertRaises(ValidationError):
            obj = TimezoneModel(timezone='invalid')
            obj.full_clean()

    def test_formfield(self):
        field = TimezoneField(default='America/Montreal')
        formfield = field.formfield()
        self.assertEqual(formfield.clean(default_timezone.zone), default_timezone)
        self.assertEqual(formfield.initial, 'America/Montreal')

    def test_choices_formfield(self):
        field = TimezoneField(default='America/Montreal', choices=COMMON_GROUPED_CHOICES)
        formfield = field.formfield()
        self.assertEqual(formfield.clean(default_timezone.zone), default_timezone)
        self.assertEqual(list(formfield.choices), list(field.choices))
        self.assertEqual(formfield.initial, 'America/Montreal')
