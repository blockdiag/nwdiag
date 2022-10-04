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

nwdiag Example
==============
following instructions shows how to generate png and svg for nwdiag

create file, ex: `nw.diag`

nw.diag is simply define nodes and transitions by dot-like text format::

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
-----

Execute nwdiag command::

   $ nwdiag nw.diag
   $ ls nw.png
   nw.png

   $ nwdiag nw.diag -T svg
   $ ls nw.svg
   nw.svg

packetdiag Example
==================
following instructions shows how to generate png and svg for packetdiag

create file, ex: `packet.diag`

::

    packetdiag {
      colwidth = 32;
      node_height = 72;

      0-15: Source Port;
      16-31: Destination Port;
      32-63: Sequence Number;
      64-95: Acknowledgment Number;
      96-99: Data Offset;
      100-105: Reserved;
      106: URG [rotate = 270];
      107: ACK [rotate = 270];
      108: PSH [rotate = 270];
      109: RST [rotate = 270];
      110: SYN [rotate = 270];
      111: FIN [rotate = 270];
      112-127: Window;
      128-143: Checksum;
      144-159: Urgent Pointer;
      160-191: (Options and Padding);
      192-223: data [colheight = 3];
    }


Usage
-----

Execute packetdiag command::

   $ packetdiag packet.diag
   $ ls packet.png
   packet.png

   $ packetdiag packet.diag -T svg
   $ ls packet.svg
   packet.svg

rackdiag Example
================
following instructions shows how to generate png and svg for rackdiag

create file, ex: `rack.diag`

::

   rackdiag {
      16U;
      1: UPS [2U];
      3: DB Server;
      4: Web Server;
      5: Web Server;
      6: Web Server;
      7: Load Balancer;
      8: L3 Switch;
   }


Usage
-----

Execute rackdiag command::

   $ rackdiag rack.diag
   $ ls rack.png
   rack.png

   $ rackdiag rack.diag -T svg
   $ ls rack.svg
   rack.svg

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
