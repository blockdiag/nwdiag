# -*- coding: utf-8 -*-

import tempfile
from nwdiag.builder import *
from nwdiag.elements import *
from nwdiag.diagparser import *
from nose.tools import raises


def __build_diagram(filename):
    import os
    testdir = os.path.dirname(__file__)
    pathname = "%s/diagrams/%s" % (testdir, filename)

    str = open(pathname).read()
    tree = parse(tokenize(str))
    return ScreenNodeBuilder.build(tree)


@raises(RuntimeError)
def test_peer_network_in_same_node_diagram():
    screen = __build_diagram('errors/peer_network_in_same_node.diag')
