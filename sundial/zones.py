from __future__ import unicode_literals

from datetime import datetime
from itertools import groupby

from django.utils.functional import lazy
from django.utils import six
from django.utils.translation import ugettext_lazy as _
import pytz

__all__ = ['COMMON_FLAT_CHOICES', 'COMMON_GROUPED_CHOICES', 'ALL_FLAT_CHOICES', 'ALL_GROUPED_CHOICES']


def _label_zone(zone):
    offset = datetime.now(pytz.timezone('/'.join(zone))).strftime('%z')
    return _("%(name)s (GMT%(offset)s)") % {
        'name': _(zone[-1].replace('_', ' ')),
        'offset': offset,
    }

_lazy_label_zone = lazy(_label_zone, six.text_type)


def _group_choices(zones):
    groups = groupby(six.moves.map(lambda z: z.split('/'), zones), lambda z: z[0])
    for group, regions in groups:
        choices = list(
            ('/'.join(region), _lazy_label_zone(region)) for region in regions
        )
        yield _(group), choices


def _flatten_grouped_choices(groups):
    for _group, choices in groups:
        # yield from choices
        for choice, value in choices:
            yield choice, value


COMMON_GROUPED_CHOICES = list(_group_choices(pytz.common_timezones))
COMMON_FLAT_CHOICES = list(_flatten_grouped_choices(COMMON_GROUPED_CHOICES))

ALL_GROUPED_CHOICES = list(_group_choices(pytz.all_timezones))
ALL_FLAT_CHOICES = list(_flatten_grouped_choices(ALL_GROUPED_CHOICES))
