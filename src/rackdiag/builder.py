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

import os
import re
from elements import *
import diagparser
from blockdiag.utils import XY


class DiagramTreeBuilder:
    def build(self, tree):
        diagram = Diagram()
        self.instantiate(diagram, tree)
        return diagram

    def instantiate(self, diagram, tree):
        for stmt in tree.stmts:
            if isinstance(stmt, diagparser.DefAttrs):
                diagram.set_attributes(stmt.attrs)

            elif isinstance(stmt, diagparser.RackItem):
                item = RackItem(stmt.number, stmt.label)
                item.set_attributes(stmt.attrs)
                diagram.nodes.append(item)


class DiagramLayoutManager:
    def __init__(self, diagram):
        self.diagram = diagram
        self.rack_usage = {}

    def run(self):
        height = self.diagram.rackheight
        for item in self.diagram.nodes:
            y = height - item.number - item.colheight
            item.xy = XY(0, y)
            self.validate_rack(item)
        self.diagram.fixiate()

    def validate_rack(self, item):
        for i in range(item.xy.y, item.xy.y + item.colheight):
            if i in self.rack_usage:
                number = self.diagram.rackheight - i
                used = self.rack_usage[i]
                print "Rack %d is already used: %s\n" % (number, used.label)
                raise
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
