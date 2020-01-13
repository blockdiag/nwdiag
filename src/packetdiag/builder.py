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

from blockdiag.utils import XY, unquote

from packetdiag import parser
from packetdiag.elements import Diagram, DiagramNode, FieldItem


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
                item = FieldItem(stmt.begin, stmt.end, unquote(stmt.label))
                item.set_attributes(stmt.attrs)

                if item.number is None:
                    if len(self.diagram.fields) == 0:
                        item.number = 0
                    else:
                        last_item = self.diagram.fields[-1]
                        item.number = last_item.number + last_item.colwidth

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
                    if self.diagram.scale_direction == "left_to_right":
                        splitted.separated_right = True
                    else:
                        splitted.separated_left = True

                    self.diagram.fields.append(splitted)

                    field.number += colwidth
                    field.colwidth -= colwidth
                    if self.diagram.scale_direction == "left_to_right":
                        field.separated_left = True
                    else:
                        field.separated_right = True

            yield field

    def run(self):
        filled = {}
        for field in self.split_field_by_column():
            x = field.number % self.diagram.colwidth
            y = field.number // self.diagram.colwidth

            if filled.get(y) is None:
                filled[y] = {}

            for rx in range(x, x + field.colwidth):
                if filled[y].get(rx):
                    msg = ("Field '%s' is conflicted to other field\n" %
                           field.label)
                    raise AttributeError(msg)
                filled[y][rx] = True

            if self.diagram.scale_direction == "right_to_left":
                x = self.diagram.colwidth - x - field.colwidth

            field.xy = XY(x, y)

        self.diagram.fixiate()


class ScreenNodeBuilder:
    @classmethod
    def build(cls, tree):
        DiagramNode.clear()
        Diagram.clear()

        return cls(tree).run()

    def __init__(self, tree):
        self.diagram = DiagramTreeBuilder().build(tree)

    def run(self):
        DiagramLayoutManager(self.diagram).run()
        return self.diagram
