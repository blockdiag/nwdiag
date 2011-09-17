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
from blockdiag.utils.XY import XY


class Diagram(blockdiag.elements.Diagram):
    def __init__(self):
        super(Diagram, self).__init__()

        self.orientation = 'portrait'
        self.node_width = 104
        self.span_width = 48
        self.span_height = 104
        self.groups = []
        self.networks = []

    def fixiate(self):
        if len(self.nodes) + len(self.networks) > 0:
            nodes = self.nodes + self.networks
            self.width = max(x.xy.x + x.width for x in nodes)
            self.height = max(x.xy.y + x.height for x in nodes)


class DiagramNode(blockdiag.elements.DiagramNode):
    def __init__(self, id):
        super(DiagramNode, self).__init__(id)

        self.address = {}
        self.networks = []

    def set_attributes(self, network, attrs):
        for attr in attrs:
            if attr.name == 'address':
                address = re.sub('\s*,\s*', '\n', unquote(attr.value))
                self.address[network] = address
            else:
                self.set_attribute(attr)


class Network(blockdiag.elements.NodeGroup):
    def __init__(self, id):
        super(Network, self).__init__(id)

        self.address = None
        self.hidden = False
        self.width = 0
        self.height = 0

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


class NodeGroup(blockdiag.elements.NodeGroup):
    def __init__(self, id):
        super(NodeGroup, self).__init__(id)

        self.layouted = False
