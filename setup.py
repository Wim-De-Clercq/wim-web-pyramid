import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'argon2_cffi',
    'marshmallow>=3.0.0rc9',
    'psycopg2',
    'pyramid',
    'pyramid_mako',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'waitress',
    'wtforms',
    'zope.sqlalchemy',
]
# Required libraries to be able to run
# Required libraries for development
extra_requires = {
    'dev': [
        'flake8',
    ],
    'deploy': [
        'alembic',
    ]
}

setup(
    name='wim_web',
    version='0.0',
    description='wim_web',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Wim De Clercq',
    author_email='',
    url='',
    keywords='web wsgi pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extra_requires,
    entry_points={
        'paste.app_factory': [
            'main = wim_web:main'
        ]
    },
)
