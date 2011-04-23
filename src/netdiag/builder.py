#!/usr/bin/python
# -*- coding: utf-8 -*-

from elements import *
import diagparser
from blockdiag.utils.XY import XY


class DiagramTreeBuilder:
    def build(self, tree):
        self.diagram = Diagram()
        self.instantiate(self.diagram, tree)
        for subgroup in self.diagram.groups:
            nodes = [n for n in self.diagram.nodes  if subgroup in n.groups]
            if len(nodes) == 0:
                self.diagram.groups.remove(subgroup)

        return self.diagram

    def instantiate(self, group, tree):
        for stmt in tree.stmts:
            if isinstance(stmt, diagparser.Node):
                node = DiagramNode.get(stmt.id)
                node.set_attributes(stmt.attrs)

                if group not in node.groups:
                    node.groups.append(group)
                if node not in self.diagram.nodes:
                    self.diagram.nodes.append(node)

            elif isinstance(stmt, diagparser.SubGraph):
                subgroup = NodeGroup.get(stmt.id)
                subgroup.level = group.level + 1

                self.diagram.groups.append(subgroup)
                self.instantiate(subgroup, stmt)

            elif isinstance(stmt, diagparser.DefAttrs):
                group.set_attributes(stmt.attrs)

            else:
                raise AttributeError("Unknown sentense: " + str(type(stmt)))

        return group


class DiagramLayoutManager:
    def __init__(self, diagram):
        self.diagram = diagram

        self.coordinates = []

    def run(self):
        self.do_layout()

    def do_layout(self):
        self.sort_networks()
        self.layout_nodes()
        self.set_network_size()

        # Slide nodes to bottom-side
        for node in self.diagram.nodes:
            node.xy = XY(node.xy.x, node.xy.y + 1)
        for network in self.diagram.groups:
            network.xy = XY(network.xy.x, network.xy.y + 1)

    def sort_networks(self):
        def compare(a, b):
            n1 = [n for n in nodes  if a in n.groups]
            n2 = [n for n in nodes  if b in n.groups]

            return cmp(len(n1), len(n2))

        for i in range(len(self.diagram.groups) - 1):
            parent = self.diagram.groups[i]
            others = self.diagram.groups[i + 1:]
            nodes = [n for n in self.diagram.nodes  if parent in n.groups]

            others.sort(compare, reverse=True)

            if self.diagram.groups[i + 1] != others[0]:
                self.diagram.groups.remove(others[0])
                self.diagram.groups.insert(i + 1, others[0])

        for i, network in enumerate(self.diagram.groups):
            network.xy = XY(0, i)

    def layout_nodes(self):
        groups = self.diagram.groups
        for node in self.diagram.nodes:
            y1 = min(groups.index(g) for g in node.groups)
            y2 = max(groups.index(g) for g in node.groups)

            for x in range(len(self.diagram.nodes)):
                points = [XY(x, y) for y in range(y1, y2 + 1)]
                if not set(points) & set(self.coordinates):
                    node.xy = XY(x, y1)
                    self.coordinates += points
                    break

    def set_network_size(self):
        for network in self.diagram.groups:
            nodes = [n for n in self.diagram.nodes  if network in n.groups]
            nodes.sort(lambda a, b: cmp(a.xy.x, b.xy.x))

            x0 = min(n.xy.x for n in nodes)
            network.xy = XY(x0, network.xy.y)

            x1 = max(n.xy.x for n in nodes)
            network.width = x1 - x0 + 1


class ScreenNodeBuilder:
    @classmethod
    def build(klass, tree):
        DiagramNode.clear()
        DiagramEdge.clear()
        NodeGroup.clear()

        diagram = DiagramTreeBuilder().build(tree)
        DiagramLayoutManager(diagram).run()
        diagram.fixiate(True)

        return diagram
