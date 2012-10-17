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
from blockdiag.utils.collections import defaultdict


class DiagramTreeBuilder:
    def build(self, tree):
        self.diagram = Diagram()
        self.instantiate(tree)

        return self.diagram

    def instantiate(self, tree):
        for stmt in tree.stmts:
            if isinstance(stmt, parser.Attr):
                self.diagram.set_attribute(stmt)
            elif isinstance(stmt, parser.FieldItem):
                item = FieldItem(stmt.number, stmt.label)
                item.set_attributes(stmt.attrs)
                self.diagram.fields.append(item)
            elif isinstance(stmt, parser.AttrPlugin):
                self.diagram.set_plugin(stmt.name, stmt.attrs)


class DiagramLayoutManager:
    def __init__(self, diagram):
        self.diagram = diagram

    def split_field_by_column(self):
        for field in self.diagram.fields:
            while True:
                x = field.number % self.diagram.colwidth
                if x + field.colwidth <= self.diagram.colwidth:
                    break
                else:
                    colwidth = self.diagram.colwidth - x

                    splitted = field.duplicate()
                    splitted.colwidth = colwidth
                    splitted.separated_right = True
                    self.diagram.fields.append(splitted)

                    field.number += colwidth
                    field.colwidth -= colwidth
                    field.separated_left = True

            yield field

    def run(self):
        filled = {}
        for field in self.split_field_by_column():
            x = field.number % self.diagram.colwidth
            y = field.number / self.diagram.colwidth

            if filled.get(y) is None:
                filled[y] = {}

            for rx in range(x, x + field.colwidth):
                if filled[y].get(rx):
                    msg = ("Field '%s' is conflicted to other field\n" %
                           field.label)
                    raise AttributeError(msg)
                filled[y][rx] = True

            field.xy = XY(x, y)

        self.diagram.fixiate()


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
