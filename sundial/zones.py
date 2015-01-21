from __future__ import unicode_literals

from datetime import datetime
from itertools import imap, groupby

from django.utils.functional import lazy
from django.utils import six
from django.utils.translation import ugettext_lazy as _
import pytz

__all__ = ['COMMON_FLAT_CHOICES', 'COMMON_GROUPED_CHOICES', 'ALL_FLAT_CHOICES', 'ALL_GROUPED_CHOICES']


def _pretty_zone(zone):
    offset = datetime.now(pytz.timezone('/'.join(zone))).strftime("%z")
    return _("%(name)s (GMT%(offset)s)") % {
        'name': _(zone[-1].replace('_', ' ')),
        'offset': offset,
    }

_lazy_pretty_zone = lazy(_pretty_zone, six.text_type)


def _grouped_choices(zones):
    groups = groupby(imap(lambda z: z.split('/'), zones), lambda z: z[0])
    for group, regions in groups:
        yield (_(group), list(('/'.join(region), _lazy_pretty_zone(region)) for region in regions))


def _flatten_choices(choices):
    for choice, value in choices:
        if isinstance(value, tuple):
            for choice, value in value:
                yield choice, value
        else:
            yield choice, value


COMMON_GROUPED_CHOICES = list(_grouped_choices(pytz.common_timezones))
COMMON_FLAT_CHOICES = list(_flatten_choices(COMMON_GROUPED_CHOICES))

ALL_GROUPED_CHOICES = list(_grouped_choices(pytz.all_timezones))
ALL_FLAT_CHOICES = list(_flatten_choices(ALL_GROUPED_CHOICES))
