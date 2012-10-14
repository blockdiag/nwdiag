# -*- coding: utf-8 -*-

from nwdiag.builder import *
from nwdiag.elements import *
from nwdiag.parser import *


def __build_diagram(filename):
    import os
    testdir = os.path.dirname(__file__)
    pathname = "%s/diagrams/%s" % (testdir, filename)

    str = open(pathname).read()
    tree = parse(tokenize(str))
    return ScreenNodeBuilder.build(tree)


def test_diagram_attributes():
    screen = __build_diagram('diagram_attributes.diag')

    assert screen.node_width == 160
    assert screen.node_height == 160
    assert screen.span_width == 32
    assert screen.span_height == 32
    assert screen.nodes[0].fontsize == 16
    assert screen.nodes[0].fontfamily == 'serif'
    assert screen.networks[0].color == (255, 0, 0)
    assert screen.networks[0].fontsize == 16
    assert screen.networks[0].fontfamily == 'serif'


def test_node_attributes():
    screen = __build_diagram('node_attributes.diag')

    network = screen.networks[0]
    assert screen.nodes[0].address[network] == '192.168.0.1'
    assert screen.nodes[1].address[network] == '192.168.0.2\n192.168.0.3'


def test_node_address_attribute():
    screen = __build_diagram('node_address_attribute.diag')

    network = screen.networks[0]
    assert screen.nodes[0].address[network] == '192.168.0.1'
    assert screen.nodes[1].address[network] == \
        '2001:0db8:bd05:01d2:288a:1fc0:0001:10ee'


def test_node_including_hyphen_diagram():
    screen = __build_diagram('node_including_hyphen.diag')

    screen.networks[0]
    assert screen.nodes[0].id == 'web-01'
    assert screen.nodes[1].id == 'web-02'


def test_single_network_diagram():
    screen = __build_diagram('single_network.diag')

    assert len(screen.nodes) == 1
    assert len(screen.networks) == 1
    assert screen.nodes[0].label == 'A'
    assert screen.nodes[0].xy == (0, 0)


def test_two_networks_diagram():
    screen = __build_diagram('two_networks.diag')

    assert_pos = {'A': (0, 0), 'B': (0, 1)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_node_belongs_to_multiple_networks_diagram():
    screen = __build_diagram('node_belongs_to_multiple_networks.diag')

    assert_pos = {'A': (0, 0)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_connected_networks_diagram():
    screen = __build_diagram('connected_networks.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 1)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_connected_networks2_diagram():
    screen = __build_diagram('connected_networks2.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (2, 0), 'D': (3, 0),
                  'E': (4, 0), 'Z': (3, 1)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_connected_networks3_diagram():
    screen = __build_diagram('connected_networks3.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (2, 0), 'D': (3, 0),
                  'E': (4, 0), 'F': (5, 0), 'G': (6, 0), 'H': (1, 1),
                  'I': (2, 1), 'J': (4, 2), 'K': (5, 2)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_group_inner_network_diagram():
    screen = __build_diagram('group_inner_network.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]

    assert len(screen.groups[0].nodes) == 2
    assert screen.groups[0].colwidth == 2
    assert screen.groups[0].colheight == 1


def test_group_outer_network_diagram():
    screen = __build_diagram('group_outer_network.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]

    assert len(screen.groups[0].nodes) == 2
    assert screen.groups[0].colwidth == 2
    assert screen.groups[0].colheight == 1


def test_group_across_network_diagram():
    screen = __build_diagram('group_across_network.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (2, 1)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]

    assert len(screen.groups[0].nodes) == 3
    assert screen.groups[0].colwidth == 3
    assert screen.groups[0].colheight == 2


def test_group_network_diagram():
    screen = __build_diagram('group_network.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (0, 1),
                  'D': (2, 1), 'E': (3, 1)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_split_group_diagram():
    screen = __build_diagram('split_group.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (3, 0),
                  'D': (2, 0), 'E': (4, 0)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_peer_network_diagram():
    screen = __build_diagram('peer_network.diag')

    assert_pos = {'A': (0, 0), 'B': (0, 1), 'C': (1, 2)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_peer_network2_diagram():
    screen = __build_diagram('peer_network2.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (1, 1)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_peer_network3_diagram():
    screen = __build_diagram('peer_network3.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (1, 1), 'D': (1, 2)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_peer_network4_diagram():
    screen = __build_diagram('peer_network4.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 1), 'C': (1, 2)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_peer_network5_diagram():
    screen = __build_diagram('peer_network5.diag')

    assert_pos = {'A': (0, 0), 'B': (1, 0), 'C': (2, 0), 'D': (2, 1)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_peer_network_branched_diagram():
    screen = __build_diagram('peer_network_branched.diag')

    assert_pos = {'A': (0, 0), 'B': (0, 1), 'C': (1, 2), 'D': (1, 3)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_same_peer_network_diagram():
    screen = __build_diagram('same_peer_network.diag')

    assert_pos = {'A': (0, 0), 'B': (0, 1), 'C': (1, 2), 'D': (0, 3)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]


def test_group_and_peer_network_diagram():
    screen = __build_diagram('group_and_peer_network.diag')

    assert_pos = {'A': (0, 0), 'B': (0, 1), 'C': (1, 2)}
    for node in screen.nodes:
        print assert_pos[node.id], node.xy
        assert node.xy == assert_pos[node.id]
