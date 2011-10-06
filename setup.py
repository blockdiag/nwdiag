# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os, sys

sys.path.insert(0, 'src')
import nwdiag

long_description = \
        open(os.path.join("src","README.txt")).read() + \
        open(os.path.join("src","TODO.txt")).read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing :: Markup",
]

setup(
     name='nwdiag',
     version=nwdiag.__version__,
     description='nwdiag generate network-diagram image file from spec-text file.',
     long_description=long_description,
     classifiers=classifiers,
     keywords=['diagram','generator'],
     author='Takeshi Komiya',
     author_email='i.tkomiya at gmail.com',
     url='http://blockdiag.com/',
     license='Apache License 2.0',
     py_modules=['sphinxcontrib_nwdiag', 'nwdiag_sphinxhelper'],
     packages=find_packages('src'),
     package_dir={'': 'src'},
     package_data = {'': ['buildout.cfg']},
     include_package_data=True,
     install_requires=[
        'setuptools',
        'PIL',
        'funcparserlib',
        'blockdiag>=0.9.3',
         # -*- Extra requirements: -*-
     ],
     extras_require=dict(
         test=[
             'Nose',
             'pep8',
         ],
         pdf=[
             'reportlab',
         ],
     ),
     test_suite='nose.collector',
     tests_require=['Nose','pep8'],
     entry_points="""
        [console_scripts]
        nwdiag = nwdiag.command:main
     """,
)

