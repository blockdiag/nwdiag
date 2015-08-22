# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from __future__ import print_function

from nwdiag.tests.utils import BuilderTestCase


class TestBuilder(BuilderTestCase):
    def test_diagram_attributes(self):
        diagram = self.build('diagram_attributes.diag')

        self.assertEqual(160, diagram.node_width)
        self.assertEqual(160, diagram.node_height)
        self.assertEqual(32, diagram.span_width)
        self.assertEqual(32, diagram.span_height)
        self.assertEqual(16, diagram.nodes[0].fontsize)
        self.assertEqual('serif', diagram.nodes[0].fontfamily)
        self.assertEqual((255, 0, 0), diagram.networks[0].color)
        self.assertEqual(16, diagram.networks[0].fontsize)
        self.assertEqual('serif', diagram.networks[0].fontfamily)

    def test_node_attributes(self):
        diagram = self.build('node_attributes.diag')

        network = diagram.networks[0]
        assert diagram.nodes[0].address[network] == '192.168.0.1'
        assert diagram.nodes[1].address[network] == '192.168.0.2\n192.168.0.3'

    def test_node_address_attribute(self):
        diagram = self.build('node_address_attribute.diag')

        network = diagram.networks[0]
        self.assertEqual('192.168.0.1',
                         diagram.nodes[0].address[network])
        self.assertEqual('2001:0db8:bd05:01d2:288a:1fc0:0001:10ee',
                         diagram.nodes[1].address[network])

    def test_node_including_hyphen_diagram(self):
        diagram = self.build('node_including_hyphen.diag')

        self.assertEqual('web-01', diagram.nodes[0].id)
        self.assertEqual('web-02', diagram.nodes[1].id)

    def test_single_network_diagram(self):
        diagram = self.build('single_network.diag')

        self.assertEqual(1, len(diagram.nodes))
        self.assertEqual(1, len(diagram.networks))
        self.assertNodeXY(diagram, {'A': (0, 0)})

    def test_two_networks_diagram(self):
        diagram = self.build('two_networks.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1)})

    def test_node_belongs_to_multiple_networks_diagram(self):
        diagram = self.build('node_belongs_to_multiple_networks.diag')
        self.assertNodeXY(diagram, {'A': (0, 0)})

    def test_connected_networks_diagram(self):
        diagram = self.build('connected_networks.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 1)})

    def test_connected_networks2_diagram(self):
        diagram = self.build('connected_networks2.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (3, 0),
                                    'E': (4, 0), 'Z': (3, 1)})

    def test_connected_networks3_diagram(self):
        diagram = self.build('connected_networks3.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (3, 0),
                                    'E': (4, 0), 'F': (5, 0),
                                    'G': (6, 0), 'H': (1, 1),
                                    'I': (2, 1), 'J': (4, 2),
                                    'K': (5, 2)})

    def test_group_inner_network_diagram(self):
        diagram = self.build('group_inner_network.diag')

        self.assertEqual(2, len(diagram.groups[0].nodes))
        self.assertEqual(2, diagram.groups[0].colwidth)
        self.assertEqual(1, diagram.groups[0].colheight)
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0)})

    def test_group_outer_network_diagram(self):
        diagram = self.build('group_outer_network.diag')

        self.assertEqual(2, len(diagram.groups[0].nodes))
        self.assertEqual(2, diagram.groups[0].colwidth)
        self.assertEqual(1, diagram.groups[0].colheight)
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0)})

    def test_group_across_network_diagram(self):
        diagram = self.build('group_across_network.diag')

        self.assertEqual(3, len(diagram.groups[0].nodes))
        self.assertEqual(3, diagram.groups[0].colwidth)
        self.assertEqual(2, diagram.groups[0].colheight)
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 1)})

    def test_group_network_diagram(self):
        diagram = self.build('group_network.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (0, 1), 'D': (2, 1),
                                    'E': (3, 1)})

    def test_split_group_diagram(self):
        diagram = self.build('split_group.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (3, 0), 'D': (2, 0),
                                    'E': (4, 0)})

    def test_peer_network_diagram(self):
        diagram = self.build('peer_network.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (1, 2)})

    def test_peer_network2_diagram(self):
        diagram = self.build('peer_network2.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1)})

    def test_peer_network3_diagram(self):
        diagram = self.build('peer_network3.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2)})

    def test_peer_network4_diagram(self):
        diagram = self.build('peer_network4.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 1),
                                    'C': (1, 2)})

    def test_peer_network5_diagram(self):
        diagram = self.build('peer_network5.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (2, 1)})

    def test_peer_network_branched_diagram(self):
        diagram = self.build('peer_network_branched.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (1, 2), 'D': (1, 3)})

    def test_same_peer_network_diagram(self):
        diagram = self.build('same_peer_network.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (1, 2), 'D': (0, 3)})

    def test_group_and_peer_network_diagram(self):
        diagram = self.build('group_and_peer_network.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (1, 2)})

    def test_peer_network_in_same_node_diagram(self):
        with self.assertRaises(RuntimeError):
            self.build('errors/peer_network_in_same_node.diag')
