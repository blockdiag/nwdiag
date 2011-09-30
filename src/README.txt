`nwdiag` generate network-diagram image file from spec-text file.

Features
========
* Generate network-diagram from dot like text (basic feature).
* Multilingualization for node-label (utf-8 only).

You can get some examples and generated images on 
`blockdiag.com <http://blockdiag.com/nwdiag/build/html/index.html>`_ .

Setup
=====

by easy_install
----------------
Make environment::

   $ easy_install nwdiag

by buildout
------------
Make environment::

   $ hg clone http://bitbucket.org/tk0miya/nwdiag
   $ cd nwdiag
   $ python bootstrap.py
   $ bin/buildout

spec-text setting sample
========================

Few examples are available.
You can get more examples at
`blockdiag.com <http://blockdiag.com/nwdiag/build/html/index.html>`_ .

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
* Python 2.4 or later (not support 3.x)
* Python Imaging Library 1.1.5 or later.
* funcparserlib 0.3.4 or later.
* setuptools or distribute.


License
=======
Apache License 2.0


History
=======

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
