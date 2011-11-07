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


class RackItem(blockdiag.elements.DiagramNode):
    def __init__(self, number, label):
        super(RackItem, self).__init__(None)
        self.number = int(number)
        self.label = label
        self.ampere = None
        self.weight = None

    @property
    def display_label(self):
        attrs = []
        if self.colheight > 1:
            attrs.append(u"%dU" % self.colheight)
        if self.ampere:
            attrs.append(u"%.1fA" % self.ampere)
        if self.weight:
            attrs.append(u"%.1fkg" % self.weight)

        labels = []
        if self.description:
            labels.append(self.description)
        if attrs:
            labels.append(u"[%s]" % u"/".join(attrs))

        return u"\n".join(labels)

    def set_attribute(self, attr):
        if re.search('^\d+U$', attr.name):
            self.colheight = int(attr.name[:-1])
        elif re.search('^\d+(\.[0-9]+)?A$', attr.name):
            self.ampere = float(attr.name[:-1])
        elif re.search('^\d+(\.[0-9]+)?kg$', attr.name):
            self.weight = float(attr.name[:-2])
        else:
            return super(RackItem, self).set_attribute(attr)

    def set_height(self, value):
        self.colheight = int(value)


class Rack(blockdiag.elements.NodeGroup):
    def __init__(self):
        super(Rack, self).__init__(None)
        self.colheight = 42
        self.description = None

    @property
    def display_label(self):
        attrs = []
        if self.description or attrs:
            attrs.insert(0, u"%dU" % self.colheight)

        labels = []
        if self.description:
            labels.append(self.description)
        if attrs:
            labels.append(u"[%s]" % u"/".join(attrs))

        return u"\n".join(labels)

    def set_attribute(self, attr):
        if re.search('^\d+U$', attr.name):
            self.colheight = int(attr.name[:-1])
        else:
            return super(Rack, self).set_attribute(attr)


class Diagram(blockdiag.elements.Diagram):
    def __init__(self):
        super(Diagram, self).__init__()

        self.racks = [Rack()]

    def set_rackheight(self, value):
        self.rack[0].colheight = int(value)

    def fixiate(self):
        self.colwidth = sum(r.colwidth for r in self.racks)
        self.colheight = max(r.colheight for r in self.racks)

    def traverse_nodes(self, **kwargs):
        for rack in self.racks:
            for node in rack.traverse_nodes():
                yield node
