from __future__ import unicode_literals


SECRET_KEY = 'not-anymore'

TIME_ZONE = 'America/Chicago'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = [
    'django.contrib.sessions',
    'sundial',
    'tests.test_fields',
    'tests.test_forms',
]

SILENCED_SYSTEM_CHECKS = ['1_7.W001']
