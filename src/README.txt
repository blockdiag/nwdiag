`nwdiag` generate network-diagram image file from spec-text file.

Features
========
* Generate network-diagram from dot like text (basic feature).
* Multilingualization for node-label (utf-8 only).

You can get some examples and generated images on 
`tk0miya.bitbucket.org <http://tk0miya.bitbucket.org/nwdiag/build/html/index.html>`_ .

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
`tk0miya.bitbucket.org <http://tk0miya.bitbucket.org/nwdiag/build/html/index.html>`_ .

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

0.2.0 (2011-05-14)
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
