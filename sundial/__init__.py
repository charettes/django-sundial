from __future__ import unicode_literals

from sundial.versioning import get_version


__all__ = ['VERSION', '__version__']

VERSION = (1, 0, 0, 'alpha', 0)

__version__ = get_version(VERSION)
