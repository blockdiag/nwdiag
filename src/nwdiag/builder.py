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
import diagparser
from blockdiag.utils.XY import XY


class DiagramTreeBuilder:
    def build(self, tree):
        self.diagram = Diagram()
        self.instantiate(self.diagram, tree)
        for subnetwork in self.diagram.networks:
            nodes = [n for n in self.diagram.nodes if subnetwork in n.networks]
            if len(nodes) == 0:
                self.diagram.networks.remove(subnetwork)

        return self.diagram

    def instantiate(self, network, tree):
        for stmt in tree.stmts:
            if isinstance(stmt, diagparser.Node):
                node = DiagramNode.get(stmt.id)
                node.set_attributes(network, stmt.attrs)

                if network not in node.networks:
                    node.networks.append(network)
                if node not in self.diagram.nodes:
                    self.diagram.nodes.append(node)

            elif isinstance(stmt, diagparser.SubGraph):
                subnetwork = NodeGroup.get(stmt.id)
                subnetwork.label = stmt.id
                subnetwork.level = network.level + 1

                if subnetwork not in self.diagram.networks:
                    self.diagram.networks.append(subnetwork)
                self.instantiate(subnetwork, stmt)

            elif isinstance(stmt, diagparser.DefAttrs):
                network.set_attributes(stmt.attrs)

            else:
                raise AttributeError("Unknown sentense: " + str(type(stmt)))

        return network


class DiagramLayoutManager:
    def __init__(self, diagram):
        self.diagram = diagram

        self.coordinates = []

    def run(self):
        self.do_layout()
        self.diagram.fixiate()

    def do_layout(self):
        self.sort_networks()
        self.layout_nodes()
        self.set_network_size()

    def sort_networks(self):
        def compare(a, b):
            n1 = [n for n in nodes  if a in n.networks]
            n2 = [n for n in nodes  if b in n.networks]

            return cmp(len(n1), len(n2))

        for i in range(len(self.diagram.networks) - 1):
            parent = self.diagram.networks[i]
            others = self.diagram.networks[i + 1:]
            nodes = [n for n in self.diagram.nodes  if parent in n.networks]

            others.sort(compare, reverse=True)

            if self.diagram.networks[i + 1] != others[0]:
                self.diagram.networks.remove(others[0])
                self.diagram.networks.insert(i + 1, others[0])

        for i, network in enumerate(self.diagram.networks):
            network.xy = XY(0, i)

    def layout_nodes(self):
        networks = self.diagram.networks
        for node in self.diagram.nodes:
            y1 = min(networks.index(g) for g in node.networks)
            y2 = max(networks.index(g) for g in node.networks)

            for x in range(len(self.diagram.nodes)):
                points = [XY(x, y) for y in range(y1, y2 + 1)]
                if not set(points) & set(self.coordinates):
                    node.xy = XY(x, y1)
                    self.coordinates += points
                    break

    def set_network_size(self):
        for network in self.diagram.networks:
            nodes = [n for n in self.diagram.nodes  if network in n.networks]
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

        return diagram
