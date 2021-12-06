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
`blockdiag.com <http://blockdiag.com/en/nwdiag/nwdiag-examples.html>`_ .

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

    nwdiag {
      network dmz {
          address = "210.x.x.x/24"

          web01 [address = "210.x.x.1"];
          web02 [address = "210.x.x.2"];
      }
      network internal {
          address = "172.x.x.x/24";

          web01 [address = "172.x.x.1"];
          web02 [address = "172.x.x.2"];
          db01;
          db02;
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
* Python 3.7 or later
* blockdiag 1.5.0 or later
* funcparserlib 0.3.6 or later
* reportlab (optional)
* wand and imagemagick (optional)
* setuptools


License
=======
Apache License 2.0
