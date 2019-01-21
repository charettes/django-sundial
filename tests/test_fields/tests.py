from __future__ import unicode_literals

from datetime import datetime

import pytz
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from sundial.fields import DateTimeField, TimezoneField
from sundial.zones import COMMON_GROUPED_CHOICES

from .models import DbTimezoneModel, TimezoneModel


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

    def test_deconstruct(self):
        # Basic deconstruction.
        field = TimezoneField(name='timezone')
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'timezone')
        self.assertEqual(path, 'sundial.fields.TimezoneField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {})

        # max_length override.
        field = TimezoneField(name='timezone', max_length=30)
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'timezone')
        self.assertEqual(path, 'sundial.fields.TimezoneField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'max_length': 30})

        # TimezoneChoices choices.
        field = TimezoneField(name='timezone', choices=COMMON_GROUPED_CHOICES)
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'timezone')
        self.assertEqual(path, 'sundial.fields.TimezoneField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'choices': COMMON_GROUPED_CHOICES})

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


class DateTimeFieldTests(TestCase):
    naive_datetime = datetime(2018, 1, 1)
    aware_datetime = timezone.make_aware(datetime(2018, 1, 1), pytz.timezone('Europe/Amsterdam'))

    @classmethod
    def setUpTestData(cls):
        cls.naive_object = DbTimezoneModel.objects.create(datetime=cls.naive_datetime)
        with override_settings(USE_TZ=True, TIME_ZONE='UTC'):
            cls.utc_object = DbTimezoneModel.objects.create(datetime=cls.aware_datetime)
        with override_settings(USE_TZ=True, TIME_ZONE='Europe/Paris'):
            cls.paris_object = DbTimezoneModel.objects.create(datetime=cls.aware_datetime)

    def assert_deconstruct_db_timezone(self, field, expected_db_timezone):
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'field')
        self.assertEqual(path, 'sundial.fields.DateTimeField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'db_timezone': expected_db_timezone})

    def test_deconstruct(self):
        field = DateTimeField(name='field')
        self.assert_deconstruct_db_timezone(field, settings.TIME_ZONE)
        with self.settings(TIME_ZONE=None):
            field = DateTimeField(name='field')
            self.assert_deconstruct_db_timezone(field, 'UTC')
        field = DateTimeField(name='field', db_timezone='Europe/Amsterdam')
        self.assert_deconstruct_db_timezone(field, 'Europe/Amsterdam')

    def test_retreival(self):
        self.naive_object.refresh_from_db()
        self.assertEqual(self.naive_object.datetime, self.naive_datetime)
        self.utc_object.refresh_from_db()
        self.assertEqual(self.utc_object.datetime, self.naive_datetime)
        with override_settings(USE_TZ=True, TIME_ZONE='UTC'):
            utc = timezone.get_current_timezone()
            self.naive_object.refresh_from_db()
            self.assertEqual(self.naive_object.datetime, self.aware_datetime)
            self.assertEqual(self.naive_object.datetime.tzinfo, utc)
            self.utc_object.refresh_from_db()
            self.assertEqual(self.utc_object.datetime, self.aware_datetime)
            self.assertEqual(self.utc_object.datetime.tzinfo, utc)
            self.paris_object.refresh_from_db()
            self.assertEqual(self.paris_object.datetime, self.aware_datetime)
            self.assertEqual(self.paris_object.datetime.tzinfo, utc)
        with override_settings(USE_TZ=True, TIME_ZONE='Europe/Paris'):
            self.naive_object.refresh_from_db()
            self.assertEqual(self.naive_object.datetime, self.aware_datetime)
            self.assertEqual(self.naive_object.datetime.tzinfo, utc)
            self.utc_object.refresh_from_db()
            self.assertEqual(self.utc_object.datetime, self.aware_datetime)
            self.assertEqual(self.utc_object.datetime.tzinfo, utc)
            self.paris_object.refresh_from_db()
            self.assertEqual(self.paris_object.datetime, self.aware_datetime)
            self.assertEqual(self.paris_object.datetime.tzinfo, utc)

    def test_lookup(self):
        self.assertSequenceEqual(
            DbTimezoneModel.objects.filter(datetime=self.naive_datetime),
            [self.naive_object, self.utc_object, self.paris_object],
        )
        with override_settings(USE_TZ=True, TIME_ZONE='UTC'):
            self.assertSequenceEqual(
                DbTimezoneModel.objects.filter(datetime=self.aware_datetime),
                [self.naive_object, self.utc_object, self.paris_object],
            )
        with override_settings(USE_TZ=True, TIME_ZONE='Europe/Paris'):
            self.assertSequenceEqual(
                DbTimezoneModel.objects.filter(datetime=self.aware_datetime),
                [self.naive_object, self.utc_object, self.paris_object],
            )
