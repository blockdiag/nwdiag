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
      A -> B -> C;
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


History
=======

1.0.3 (2014-07-03)
------------------
* rackdiag: Fix rackheight syntax (cf. rack { 12U }) was disabled

1.0.2 (2014-07-02)
------------------
* Change interface of docutils node (for sphinxcontrib module)

1.0.1 (2014-06-26)
------------------
* Add options to blockdiag directive (docutils extension)
   - :width:
   - :height:
   - :scale:
   - :align:
   - :name:
   - :class:
   - :figwidth:
   - :figclass:

1.0.0 (2013-10-05)
------------------
* Support python 3.2 and 3.3 (thanks to @masayuko)
* Drop supports for python 2.4 and 2.5
* Replace dependency: PIL -> Pillow

0.9.4 (2012-12-20)
------------------
* Fix bugs

0.9.3 (2012-12-17)
------------------
* [rackdiag] Allow multiple rackitems in same level
* Fix bugs

0.9.2 (2012-11-17)
------------------
* [rackdiag] Add auto-numbering feature
* Fix bugs

0.9.1 (2012-10-28)
------------------
* Fix bugs

0.9.0 (2012-10-22)
------------------
* Optimize algorithm for rendering shadow
* Add options to docutils directive
* [packetdiag] represent splitted packets with dashed-line
* Fix bugs

0.8.2 (2012-09-29)
------------------
* Fix bugs

0.8.1 (2012-09-08)
------------------
* Add packetdiag_sphinxhelper

0.8.0 (2012-09-06)
------------------
* Add packetdiag which supports generating packet-header diaagram
* [nwdiag] Add diagram attribute: external_connector
* Update to new package structure (blockdiag >= 1.1.2)
* Allow # to comment syntax
* Fix bugs

0.7.0 (2011-11-19)
------------------
* Accept N/A rack-unit
* Add fontfamily attribute for switching fontface
* Fix bugs

0.6.1 (2011-11-06)
------------------
* [rackdiag] Support multiple racks rendering 
* [rackdiag] Add rack attribute: unit-height, weight, ampere, ascending
* [rackdiag] Support putting multiple items to same rack-unit

0.6.0 (2011-11-06)
------------------
* Add rackdiag which supports genarating rack-structure diagram
* Add docutils extension
* Fix bugs

0.5.3 (2011-11-01)
------------------
* Add class feature (experimental)

0.5.2 (2011-11-01)
------------------
* Follow blockdiag-0.9.7 interface

0.5.1 (2011-10-19)
------------------
* Follow blockdiag-0.9.5 interface

0.5.0 (2011-10-07)
------------------
* Change shape of trunkline like a pipeline
* Add network attribute: color
* Add diagram attribute: default_network_color

0.4.2 (2011-09-30)
------------------
* Add diagram attributes: default_text_color
* Fix bugs

0.4.1 (2011-09-26)
------------------
* Add diagram attributes: default_node_color, default_group_color and default_line_color
* Fix bugs

0.4.0 (2011-08-09)
------------------
* Add syntax for peer network

0.3.3 (2011-08-07)
------------------
* Add syntax for peer network (experimental)
* Fix bugs

0.3.2 (2011-08-03)
------------------
* Fix bugs

0.3.1 (2011-08-01)
------------------
* Fix bugs

0.3.0 (2011-07-18)
------------------
* Upgrade layout engine
* Allow to note ip addresses directly
* Allow node_id including hyphen chars
* Fix bugs

0.2.7 (2011-07-05)
------------------
* Fix bugs

0.2.6 (2011-07-03)
------------------
* Allow "." to id token
* Support input from stdin
* Support multiple node address (using comma)
* Do not sort networks (ordered as declarations)
* Fix bugs

0.2.5 (2011-06-29)
------------------
* Adjust parameters for span and margin

0.2.4 (2011-05-17)
------------------
* Add --version option
* Fix bugs

0.2.3 (2011-05-15)
------------------
* Fix bugs

0.2.2 (2011-05-15)
------------------
* Implement grouping nodes

0.2.1 (2011-05-14)
------------------
* Change license to Apache License 2.0
* Support blockdiag 0.8.1 core interface 

0.2.0 (2011-05-02)
------------------
* Rename package to nwdiag

0.1.6 (2011-04-30)
------------------
* Fix bugs

0.1.5 (2011-04-26)
------------------
* Fix bugs

0.1.4 (2011-04-25)
------------------
* Implement jumped edge
* Fix bugs

0.1.3 (2011-04-23)
------------------
* Fix sphinxcontrib_netdiag was not worked

0.1.2 (2011-04-23)
------------------
* Support multi-homed host
* Drop network-bridge sytanx (cf. net_a -- net_b)

0.1.1 (2011-04-10)
------------------
* Fix bugs

0.1.0 (2011-04-09)
------------------
* First release
