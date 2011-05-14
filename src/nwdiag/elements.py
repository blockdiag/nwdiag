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
        self.span_height = 120
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
                self.address[network] = unquote(attr.value)
            else:
                self.set_attribute(attr)


class Network(blockdiag.elements.NodeGroup):
    def __init__(self, id):
        super(Network, self).__init__(id)

        self.address = None

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
