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
    classifiers=[
    ],
)
