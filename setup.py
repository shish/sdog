import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = ""  # open(os.path.join(here, 'CHANGES.txt')).read()

setup(
    name='SDog',
    version='0.2.2',
    description='SDog',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Shish',
    author_email='webmaster+sdog@shishnet.org',
    url='http://github.com/shish/sdog',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='sdog',
    install_requires=[],
    extras_require = {
        'title': ["setproctitle"],
    },
    entry_points="""
        [console_scripts]
        sdog = sdog.monitor:main
    """,
    )
