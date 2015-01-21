from __future__ import unicode_literals

from setuptools import find_packages, setup

import sundial


version = sundial.__version__
requirements = ['django>=1.6', 'pytz']

setup(
    name='django-sundial',
    version=version,
    url='https://github.com/charettes/django-sundial',
    author='Simon Charette.',
    author_email='charette.s+sundial@gmail.com',
    description='',
    license='MIT',
    packages=find_packages('sundial'),
    install_requires=requirements,
    extras_require={
        ['south']: ['south']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
