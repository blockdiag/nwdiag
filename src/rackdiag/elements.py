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

from __future__ import division

import re

import blockdiag.elements
from blockdiag.utils import XY

from rackdiag.utils.math import lcm


class DiagramNode(blockdiag.elements.DiagramNode):
    pass


class RackItem(blockdiag.elements.DiagramNode):
    desctable = []
    attrname = {}

    @classmethod
    def clear(cls):
        super(RackItem, cls).clear()
        cls.desctable = ['number', 'label', 'units', 'ampere',
                         'weight', 'description']
        cls.attrname = dict(number='No', label='Name', units='Height',
                            ampere='Capacity', weight='Weight',
                            description='Description')

    def __init__(self, number, label):
        super(RackItem, self).__init__(None)
        self.number = int(number)
        self.label = label
        self.ampere = None
        self.weight = None

        if self.label == 'N/A':
            self.color = 'gray'

    @property
    def display_label(self):
        attrs = []
        if self.colheight > 1:
            attrs.append("%dU" % self.colheight)
        if self.ampere:
            attrs.append("%.1fA" % self.ampere)
        if self.weight:
            attrs.append("%.1fkg" % self.weight)

        labels = []
        if self.label:
            labels.append(self.label)
        if attrs:
            labels.append("[%s]" % "/".join(attrs))

        return "\n".join(labels)

    def set_attribute(self, attr):
        if re.search(r'^\d+U$', attr.name):
            self.colheight = int(attr.name[:-1])
        elif re.search(r'^\d+(\.[0-9]+)?A$', attr.name):
            self.ampere = float(attr.name[:-1])
        elif re.search(r'^\d+(\.[0-9]+)?kg$', attr.name):
            self.weight = float(attr.name[:-2])
        else:
            return super(RackItem, self).set_attribute(attr)

    def set_height(self, value):
        self.colheight = int(value)

    def to_desctable(self):
        attrs = []
        for name in self.desctable:
            if name == 'units':
                attrs.append("%dU" % self.colheight)
            elif name == 'ampere':
                if self.ampere is None:
                    attrs.append("")
                else:
                    attrs.append(("%.1fA" % self.ampere) or "")
            elif name == 'weight':
                if self.weight is None:
                    attrs.append("")
                else:
                    attrs.append(("%.1fkg" % self.weight) or "")
            else:
                value = getattr(self, name)
                if value is None:
                    attrs.append("")
                elif isinstance(value, int):
                    attrs.append(str(value))
                else:
                    attrs.append(getattr(self, name))

        return attrs


class Rack(blockdiag.elements.NodeGroup):
    def __init__(self):
        super(Rack, self).__init__(None)
        self.colheight = 42
        self.description = None
        self.descending = True

    def set_default_fontsize(self, value):
        raise AttributeError()  # Ignore and pass-through to Diagram

    @property
    def display_label(self):
        attrs = []
        if self.description or attrs:
            attrs.insert(0, "%dU" % self.colheight)

        labels = []
        if self.description:
            labels.append(self.description)
        if attrs:
            labels.append("[%s]" % "/".join(attrs))

        return "\n".join(labels)

    def items(self, levels):
        if isinstance(levels, int):
            levels = [levels]

        return [node for node in self.nodes if node.xy.y in levels]

    def get_linked_levels(self, level):
        def get_max_height(self, y):
            try:
                return max(n.colheight for n in self.items(y))
            except Exception:
                return 0

        height = get_max_height(self, level)
        for dy in range(1, self.colheight - level + 1):
            if dy < height:
                height = max(height, get_max_height(self, level + dy) + dy)

        return range(level, level + height)

    def adjust_node_widths(self):
        i = 0
        linked_widths = {}
        widths = []
        while i < self.colheight:
            levels = self.get_linked_levels(i)

            if levels:
                linked_widths[i] = []
                for level in levels:
                    nodes = self.items(level)
                    if nodes:
                        width = max(n.xy.x for n in nodes) + 1
                        widths.append(width)
                        linked_widths[i].append(width)

                i += len(levels)
            else:
                i += 1

        i = 0
        self.colwidth = lcm(*widths) or 1
        while i < self.colheight:
            levels = self.get_linked_levels(i)

            if levels:
                colwidth = max(linked_widths[i]) or 1
                for level in levels:
                    nodes = self.items(level)
                    if nodes:
                        width = self.colwidth // colwidth
                        for node in nodes:
                            node.xy = XY(node.xy.x * width, node.xy.y)
                            node.colwidth = width

                i += len(levels)
            else:
                i += 1

    def fixiate(self):
        self.adjust_node_widths()

        for node in self.nodes:
            node.xy = node.xy.shift(x=self.xy.x)

    def set_ascending(self, attr):
        self.descending = False

    def set_attribute(self, attr):
        if re.search(r'^\d+U$', attr.name):
            self.colheight = int(attr.name[:-1])
        else:
            return super(Rack, self).set_attribute(attr)


class Diagram(blockdiag.elements.Diagram):
    _DiagramNode = RackItem

    @classmethod
    def clear(cls):
        super(Diagram, cls).clear()
        cls._DiagramNode.clear()

    def __init__(self):
        super(Diagram, self).__init__()

        self.racks = [Rack()]

    def set_default_fontsize(self, value):
        super(Diagram, self).set_default_fontsize(value)
        self.fontsize = int(value)

    def set_rackheight(self, value):
        self.racks[0].colheight = int(value)

    def fixiate(self):
        self.colwidth = sum(r.colwidth for r in self.racks)
        self.colheight = max(r.colheight for r in self.racks)

    def traverse_nodes(self, **kwargs):
        for rack in self.racks:
            for node in rack.traverse_nodes():
                yield node
