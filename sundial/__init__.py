from __future__ import unicode_literals

from django.utils import version


__all__ = ['VERSION', '__version__']

VERSION = (1, 0, 4, 'final', 0)

__version__ = version.get_version(VERSION)
