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

from elements import *
import parser
from blockdiag.utils import XY


class DiagramTreeBuilder:
    def build(self, tree):
        self.diagram = Diagram()
        self.instantiate(self.diagram.racks[0], tree)

        for rack in self.diagram.racks[:]:
            if len(rack.nodes) == 0:
                self.diagram.racks.remove(rack)

        return self.diagram

    def instantiate(self, rack, tree):
        for stmt in tree.stmts:
            if isinstance(stmt, parser.Attr):
                try:
                    rack.set_attribute(stmt)
                except AttributeError:
                    self.diagram.set_attribute(stmt)
            elif isinstance(stmt, parser.RackItem):
                item = RackItem(stmt.number, stmt.label)
                item.set_attributes(stmt.attrs)
                rack.nodes.append(item)
            elif isinstance(stmt, parser.Rack):
                _rack = Rack()
                self.diagram.racks.append(_rack)
                self.instantiate(_rack, stmt)
            elif isinstance(stmt, parser.AttrPlugin):
                self.diagram.set_plugin(stmt.name, stmt.attrs)


class DiagramLayoutManager:
    def __init__(self, diagram):
        self.diagram = diagram
        self.rack_usage = {}

    def run(self):
        rack_x = 0
        for rack in self.diagram.racks:
            self.rack_usage = {}

            for item in rack.nodes:
                item.xy = XY(-1, -1)

            for item in rack.nodes:
                if rack.descending:
                    y = rack.colheight - item.number - item.colheight + 1
                else:
                    y = item.number - 1

                nodes = [n for n in rack.nodes if n.xy.y == y]
                if nodes:
                    x = max(n.xy.x for n in nodes) + 1
                else:
                    x = 0

                item.xy = XY(x, y)
                self.validate_rack(item)
            rack.xy = XY(rack_x, 0)
            rack.fixiate()

            rack_x += rack.colwidth

        self.diagram.fixiate()

    def validate_rack(self, item):
        if item.xy.y < 0:
            msg = "Rack %d is oversized to rack-height\n" % item.number
            raise AttributeError(msg)

        for i in range(item.xy.y, item.xy.y + item.colheight):
            if i in self.rack_usage:
                if self.rack_usage[i].colheight == item.colheight == 1:
                    pass
                else:
                    used = self.rack_usage[i].label.encode('utf-8')
                    msg = "Rack %d is already used: %s\n" % (item.number, used)
                    raise AttributeError(msg)
            else:
                self.rack_usage[i] = item


class ScreenNodeBuilder:
    @classmethod
    def build(cls, tree):
        DiagramNode.clear()
        DiagramEdge.clear()
        NodeGroup.clear()
        Diagram.clear()

        return cls(tree).run()

    def __init__(self, tree):
        self.diagram = DiagramTreeBuilder().build(tree)

    def run(self):
        DiagramLayoutManager(self.diagram).run()
        return self.diagram
