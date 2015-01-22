from __future__ import unicode_literals

from setuptools import find_packages, setup

import sundial


with open('README.rst') as file_:
    long_description = file_.read()

setup(
    name='django-sundial',
    version=sundial.__version__,
    description='Django application providing database, form fields and middleware for timezone support.',
    long_description=long_description,
    url='https://github.com/charettes/django-sundial',
    author='Simon Charette.',
    author_email='charette.s+sundial@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
    keywords=['django timezone'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['django>=1.6', 'pytz'],
    extras_require={
        'south': ['south'],
        'tests': ['tox'],
    },
)
