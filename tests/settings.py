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
