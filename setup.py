# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

sys.path.insert(0, 'src')
import nwdiag

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing :: Markup",
]

requires = ['blockdiag>=1.5.0']
test_requires = ['nose',
                 'pep8>=1.3',
                 'flake8',
                 'flake8-coding',
                 'flake8-copyright',
                 'reportlab',
                 'docutils']

setup(
    name='nwdiag',
    version=nwdiag.__version__,
    description='nwdiag generates network-diagram image from text',
    long_description=open("README.rst").read(),
    classifiers=classifiers,
    keywords=['diagram', 'generator'],
    author='Takeshi Komiya',
    author_email='i.tkomiya at gmail.com',
    url='http://blockdiag.com/',
    download_url='http://pypi.python.org/pypi/nwdiag',
    license='Apache License 2.0',
    py_modules=[
        'nwdiag_sphinxhelper',
        'rackdiag_sphinxhelper',
        'packetdiag_sphinxhelper',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['buildout.cfg']},
    include_package_data=True,
    install_requires=requires,
    extras_require=dict(
        testing=test_requires,
        pdf=[
            'reportlab',
        ],
        rst=[
            'docutils',
        ],
    ),
    test_suite='nose.collector',
    tests_require=test_requires,
    entry_points="""
       [console_scripts]
       nwdiag = nwdiag.command:main
       rackdiag = rackdiag.command:main
       packetdiag = packetdiag.command:main

       [blockdiag_noderenderer]
       _packet_node = packetdiag.noderenderers
    """,
)
