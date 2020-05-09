from datetime import datetime
from itertools import groupby

import pytz
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

__all__ = ['COMMON_CHOICES', 'COMMON_GROUPED_CHOICES', 'ALL_CHOICES', 'ALL_GROUPED_CHOICES']


def _label_zone(zone):
    offset = datetime.now(pytz.timezone('/'.join(zone))).strftime('%z')
    return _("%(name)s (GMT%(offset)s)") % {
        'name': _(zone[-1].replace('_', ' ')),
        'offset': offset,
    }


_lazy_label_zone = lazy(_label_zone, str)


def _group_choices(zones):
    groups = groupby(map(lambda z: z.split('/'), zones), lambda z: z[0])
    for group, regions in groups:
        yield _(group), [
            ('/'.join(region), _lazy_label_zone(region)) for region in regions
        ]


def _flatten_choices(groups):
    for _group, choices in groups:
        yield from choices


class TimezoneChoices:
    def __init__(self, name, grouped=False):
        self.name = name
        self.grouped = grouped
        zones = getattr(pytz, "%s_timezones" % name)
        choices = _group_choices(zones)
        if not grouped:
            choices = _flatten_choices(choices)
        self._choices = list(choices)

    def __iter__(self):
        return iter(self._choices)

    def __getitem__(self, key):
        return self._choices[key]

    def deconstruct(self):
        kwargs = {'grouped': True} if self.grouped else {}
        return 'sundial.zones.TimezoneChoices', (self.name,), kwargs


COMMON_CHOICES = TimezoneChoices('common')
COMMON_GROUPED_CHOICES = TimezoneChoices('common', grouped=True)

ALL_CHOICES = TimezoneChoices('all')
ALL_GROUPED_CHOICES = TimezoneChoices('all', grouped=True)
