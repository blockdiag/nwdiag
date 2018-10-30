`nwdiag` generate network-diagram image file from spec-text file.

.. image:: https://drone.io/bitbucket.org/blockdiag/nwdiag/status.png
   :target: https://drone.io/bitbucket.org/blockdiag/nwdiag
   :alt: drone.io CI build status

.. image:: https://pypip.in/v/nwdiag/badge.png
   :target: https://pypi.python.org/pypi/nwdiag/
   :alt: Latest PyPI version

.. image:: https://pypip.in/d/nwdiag/badge.png
   :target: https://pypi.python.org/pypi/nwdiag/
   :alt: Number of PyPI downloads


Features
========
* Generate network-diagram from dot like text (basic feature).
* Multilingualization for node-label (utf-8 only).

You can get some examples and generated images on 
`blockdiag.com <http://blockdiag.com/nwdiag/build/html/index.html>`_ .

Setup
=====

Use easy_install or pip::

   $ sudo easy_install nwdiag

   Or

   $ sudo pip nwdiag


spec-text setting sample
========================

Few examples are available.
You can get more examples at
`blockdiag.com`_ .

simple.diag
------------

simple.diag is simply define nodes and transitions by dot-like text format::

    diagram {
      lane you {
        A; B;
      }
      lane me {
        C;
      }
    }


Usage
=====

Execute nwdiag command::

   $ nwdiag simple.diag
   $ ls simple.png
   simple.png


Requirements
============
* Python 2.6, 2.7, 3.2, 3.3, 3.4
* Pillow 2.2.1 or later
* funcparserlib 0.3.6 or later
* reportlab (optional)
* wand and imagemagick (optional)
* setuptools


License
=======
Apache License 2.0
