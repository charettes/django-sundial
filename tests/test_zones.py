from __future__ import unicode_literals

from datetime import datetime

import pytz
from django.test import SimpleTestCase
from django.utils.encoding import force_text

from sundial import zones


class TimezoneChoicesTests(SimpleTestCase):
    def test_label_offset(self):
        for value, label in zones.ALL_CHOICES:
            offset = datetime.now(pytz.timezone(value)).strftime('%z')
            self.assertIn(offset, force_text(label))

    def test_slicing(self):
        self.assertEqual(len(zones.ALL_CHOICES[0:3]), 3)

    def test_indexing(self):
        self.assertIsInstance(zones.ALL_CHOICES[0], tuple)

    def test_deconstruction(self):
        expected_path = "%s.%s" % (
            zones.TimezoneChoices.__module__,
            zones.TimezoneChoices.__name__,
        )
        path, args, kwargs = zones.ALL_CHOICES.deconstruct()
        self.assertEqual(path, expected_path)
        self.assertEqual(args, ('all',))
        self.assertEqual(kwargs, {})
        path, args, kwargs = zones.ALL_GROUPED_CHOICES.deconstruct()
        self.assertEqual(path, expected_path)
        self.assertEqual(args, ('all',))
        self.assertEqual(kwargs, {'grouped': True})
        path, args, kwargs = zones.COMMON_CHOICES.deconstruct()
        self.assertEqual(path, expected_path)
        self.assertEqual(args, ('common',))
        self.assertEqual(kwargs, {})
        path, args, kwargs = zones.COMMON_GROUPED_CHOICES.deconstruct()
        self.assertEqual(path, expected_path)
        self.assertEqual(args, ('common',))
        self.assertEqual(kwargs, {'grouped': True})
