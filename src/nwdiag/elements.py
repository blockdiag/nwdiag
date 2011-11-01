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

import re
import sys
import blockdiag.elements
from blockdiag.elements import *
from blockdiag.utils import images, XY


class DiagramNode(blockdiag.elements.DiagramNode):
    def __init__(self, id):
        super(DiagramNode, self).__init__(id)

        self.address = {}
        self.networks = []
        self.layouted = False

    def set_attributes(self, network, attrs):
        for attr in attrs:
            if attr.name == 'address':
                address = re.sub('\s*,\s*', '\n', unquote(attr.value))
                self.address[network] = address
            else:
                self.set_attribute(attr)


class Network(blockdiag.elements.NodeGroup):
    basecolor = (185, 203, 228)
    linecolor = (0, 0, 0)

    @classmethod
    def set_default_line_color(cls, color):
        cls.linecolor = images.color_to_rgb(color)

    @classmethod
    def clear(cls):
        super(Network, cls).clear()
        cls.basecolor = (185, 203, 228)
        cls.linecolor = (0, 0, 0)

    def __init__(self, id):
        super(Network, self).__init__(id)

        self.address = None
        self.hidden = False
        self.colwidth = 1
        self.colheight = 1

    @classmethod
    def create_anonymous(klass, nodes, attrs=[]):
        if len(set(nodes)) != len(nodes):
            msg = "Do not connect same node to peer network: %s"
            raise RuntimeError(msg % nodes[0].id)

        # search networks including same nodes
        is_same = lambda nw: set(nodes) & set(nw.nodes) == set(nodes)
        same = [nw for nw in nodes[0].networks if nw.hidden and is_same(nw)]
        if [nw for nw in nodes[0].networks if nw.hidden and is_same(nw)]:
            return None

        network = klass(None)
        network.hidden = True
        for node in nodes:
            node.networks.append(network)
            network.nodes.append(node)

        if attrs:
            node.set_attributes(network, attrs)

        return network

    @property
    def display_label(self):
        if self.label:
            if self.address:
                label = "%s\n%s" % (self.label, self.address)
            else:
                label = self.label
        else:
            label = self.address

        return label


class Route(blockdiag.elements.DiagramEdge):
    pass


class Diagram(blockdiag.elements.Diagram):
    _DiagramNode = DiagramNode
    _Network = Network
    _Route = Route

    def set_default_line_color(self, color):
        super(Diagram, self).set_default_line_color(color)
        self._Network.set_default_line_color(self.linecolor)

    def set_default_network_color(self, color):
        color = images.color_to_rgb(color)
        self._Network.set_default_color(color)

    def __init__(self):
        super(Diagram, self).__init__()

        self.orientation = 'portrait'
        self.node_width = 104
        self.span_width = 48
        self.span_height = 104
        self.groups = []
        self.networks = []
        self.routes = []

    def fixiate(self):
        if len(self.nodes) + len(self.networks) > 0:
            nodes = self.nodes + self.networks
            self.colwidth = max(x.xy.x + x.colwidth for x in nodes)
            self.colheight = max(x.xy.y + x.colheight for x in nodes)
