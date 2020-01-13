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

import blockdiag.elements
from blockdiag.utils import images, unquote


class NodeGroup(blockdiag.elements.NodeGroup):
    pass


class DiagramNode(blockdiag.elements.DiagramNode):
    def __init__(self, _id):
        super(DiagramNode, self).__init__(_id)

        self.address = {}
        self.networks = []
        self.layouted = False

    def set_attributes(self, network, attrs=None):
        if attrs is None:
            attrs, network = network, None

        for attr in attrs:
            if attr.name == 'address':
                address = re.sub(r'\s*,\s*', '\n', unquote(attr.value))
                self.address[network] = address
            else:
                self.set_attribute(attr)


class DiagramEdge(blockdiag.elements.DiagramEdge):
    pass


class Network(blockdiag.elements.NodeGroup):
    basecolor = (185, 203, 228)
    linecolor = (0, 0, 0)

    @classmethod
    def set_default_linecolor(cls, color):
        cls.linecolor = images.color_to_rgb(color)

    @classmethod
    def set_default_textcolor(cls, color):
        cls.textcolor = images.color_to_rgb(color)

    @classmethod
    def clear(cls):
        super(Network, cls).clear()
        cls.basecolor = (185, 203, 228)
        cls.linecolor = (0, 0, 0)

    def __init__(self, _id):
        super(Network, self).__init__(_id)

        self.address = None
        self.hidden = False
        self.colwidth = 1
        self.colheight = 1

    @classmethod
    def create_anonymous(cls, nodes, attrs=None):
        def is_same(nw):
            return set(nodes) & set(nw.nodes) == set(nodes)

        if len(set(nodes)) != len(nodes):
            msg = "Do not connect same node to peer network: %s"
            raise RuntimeError(msg % nodes[0].id)

        # search networks including same nodes
        if [nw for nw in nodes[0].networks if nw.hidden and is_same(nw)]:
            return None

        network = cls(None)
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

    def set_default_linecolor(self, color):
        super(Diagram, self).set_default_linecolor(color)
        self._Network.set_default_linecolor(self.linecolor)

    def set_default_textcolor(self, color):
        super(Diagram, self).set_default_textcolor(color)
        self._Network.set_default_text_color(self.textcolor)

    def set_default_fontsize(self, fontsize):
        super(Diagram, self).set_default_fontsize(fontsize)
        self._Network.set_default_fontsize(fontsize)

    def set_default_fontfamily(self, familyname):
        super(Diagram, self).set_default_fontfamily(familyname)
        self._Network.set_default_fontfamily(familyname)

    def set_default_network_color(self, color):
        color = images.color_to_rgb(color)
        self._Network.set_default_color(color)

    def __init__(self):
        super(Diagram, self).__init__()

        self.orientation = 'portrait'
        self.external_connector = True
        self.groups = []
        self.networks = []
        self.routes = []

    def set_external_connector(self, value):
        value = value.lower()
        if value == 'none':
            self.external_connector = False
        else:
            msg = "unknown external connector: %s\n" % value
            raise AttributeError(msg)

    def fixiate(self):
        self.colwidth = max(n.xy.x + n.colwidth for n in self.nodes)
        self.colheight = max(n.xy.y + n.colheight for n in self.nodes)

        colheight = max(nw.xy.y + nw.colheight - 1 for nw in self.networks)
        if self.colheight < colheight:
            self.colheight = colheight
