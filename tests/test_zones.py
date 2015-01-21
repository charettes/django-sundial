from __future__ import unicode_literals

from datetime import datetime
from django.test import SimpleTestCase
from django.utils.encoding import force_text
import pytz

from sundial.zones import ALL_FLAT_CHOICES


class ZonesTests(SimpleTestCase):
    def test_label_offset(self):
        for value, label in ALL_FLAT_CHOICES:
            offset = datetime.now(pytz.timezone(value)).strftime('%z')
            self.assertIn(offset, force_text(label))
