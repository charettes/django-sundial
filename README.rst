django-sundial
==============

.. image:: https://pypip.in/license/django-sundial/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-sundial/
    :alt: License

.. image:: https://pypip.in/version/django-sundial/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-sundial/
    :alt: Latest Version

.. image:: https://travis-ci.org/charettes/django-sundial.svg?branch=master
    :target: https://travis-ci.org/charettes/django-sundial
    :alt: Build Status

.. image:: https://coveralls.io/repos/charettes/django-sundial/badge.svg?branch=master
    :target: https://coveralls.io/r/charettes/django-sundial?branch=master
    :alt: Coverage Status

.. image:: https://pypip.in/py_versions/django-sundial/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-sundial/
    :alt: Supported Python Versions

.. image:: https://pypip.in/wheel/django-sundial/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-sundial/
    :alt: Wheel Status

Django application providing database, form fields and middleware for timezone support.

Installation
------------

.. code:: sh

    pip install django-sundial

Usage
-----

.. code:: python

    # settings.py
    TIME_ZONE = 'America/Chicago'
    AUTH_USER_MODEL = 'app.User'
    MIDDLEWARE = [
        ...,
        'django.contrib.sessions.middleware.SessionMiddleware',
        ...,
        'sundial.middleware.TimezoneMiddleware',
        ...,
    ]

.. code:: python

    # app/models.py
    from django.conf import settings
    from django.contrib.auth.models import AbstractUser
    from django.contrib.auth.signals import user_logged_in
    from django.dispatch.dispatcher import receiver

    from sundial.fields import TimezoneField
    from sundial.utils import set_session_timezone
    from sundial.zones import COMMON_GROUPED_CHOICES

    class User(AbstractUser):
        timezone = TimezoneField(
            default=settings.TIME_ZONE, choices=COMMON_GROUPED_CHOICES
        )

    @receiver(user_logged_in)
    def assign_user_timezone(request, user, **kwargs):
        set_session_timezone(request.session, user.timezone)
