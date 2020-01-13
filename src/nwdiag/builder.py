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

from collections import namedtuple

from blockdiag.utils import XY, unquote

from nwdiag import parser
from nwdiag.elements import (Diagram, DiagramEdge, DiagramNode, Network,
                             NodeGroup, Route)


class DiagramTreeBuilder:
    def build(self, tree):
        self.diagram = Diagram()
        self.instantiate(None, None, tree)
        for network in self.diagram.networks:
            nodes = [n for n in self.diagram.nodes if network in n.networks]
            if len(nodes) == 0:
                self.diagram.networks.remove(network)

        for i, network in enumerate(self.diagram.networks):
            network.xy = XY(0, i)

        for subgroup in self.diagram.groups:
            if len(subgroup.nodes) == 0:
                self.diagram.groups.remove(subgroup)

        for node in self.diagram.nodes:
            if len(node.networks) == 0:
                msg = "DiagramNode %s does not belong to any networks"
                raise RuntimeError(msg % node.id)

        # show networks including same nodes
        for nw in self.diagram.networks:
            if nw.hidden and len(nw.nodes) == 2:
                def is_same(x):
                    return set(nodes) & set(x.nodes) == set(nodes)

                nodes = nw.nodes
                for n in self.diagram.networks:
                    if n != nw and is_same(n):
                        nw.hidden = False
                        break

        # show network for multiple peer networks from same node
        nodes = []
        for nw in self.diagram.networks:
            if nw.hidden and len(nw.nodes) == 2:
                nodes.append(nw.nodes[0])  # parent node (FROM node)

        for node in [n for n in set(nodes) if nodes.count(n) > 1]:
            for network in node.networks:
                if len(network.nodes) == 2:
                    network.hidden = False

        return self.diagram

    def instantiate(self, network, group, tree):
        for stmt in tree.stmts:
            if isinstance(stmt, parser.Node):
                node = DiagramNode.get(stmt.id)
                node.set_attributes(network, stmt.attrs)

                if group:
                    if (node.group and node.group != self.diagram and
                       (group != node.group)):
                        msg = "DiagramNode could not belong to two groups"
                        raise RuntimeError(msg)
                    node.group = group
                    group.nodes.append(node)
                elif node.group is None:
                    node.group = self.diagram

                if network is not None:
                    if network not in node.networks:
                        node.networks.append(network)
                    if node not in network.nodes:
                        network.nodes.append(node)
                if node not in self.diagram.nodes:
                    self.diagram.nodes.append(node)

            elif isinstance(stmt, parser.Network):
                subnetwork = Network.get(stmt.id)
                subnetwork.label = stmt.id

                if subnetwork not in self.diagram.networks:
                    self.diagram.networks.append(subnetwork)

                substmt = namedtuple('Statements', 'stmts')([])
                for s in stmt.stmts:
                    if isinstance(s, parser.Attr):
                        subnetwork.set_attribute(s)
                    else:
                        substmt.stmts.append(s)

                self.instantiate(subnetwork, group, substmt)

            elif isinstance(stmt, parser.Group):
                subgroup = NodeGroup.get(stmt.id)

                if subgroup not in self.diagram.groups:
                    self.diagram.groups.append(subgroup)

                substmt = namedtuple('Statements', 'stmts')([])
                for s in stmt.stmts:
                    if isinstance(s, parser.Attr):
                        subgroup.set_attribute(s)
                    else:
                        substmt.stmts.append(s)

                self.instantiate(network, subgroup, substmt)

            elif isinstance(stmt, parser.Peer):
                nodes = []
                for edge in stmt.edges:
                    nodes.append(DiagramNode.get(edge.from_node))
                    nodes.append(DiagramNode.get(edge.to_node))

                for node in nodes:
                    if node.group is None:
                        node.group = self.diagram
                    if node not in self.diagram.nodes:
                        self.diagram.nodes.append(node)

                if len(nodes[0].networks) == 0:
                    nw = Network.create_anonymous([nodes[0]])
                    if nw:
                        self.diagram.networks.append(nw)

                for edge in stmt.edges:
                    from_node = DiagramNode.get(edge.from_node)
                    to_node = DiagramNode.get(edge.to_node)

                    _nodes = [from_node, to_node]
                    nw = Network.create_anonymous(_nodes, edge.attrs)
                    if nw:
                        self.diagram.networks.append(nw)

            elif isinstance(stmt, parser.Route):
                nodes = [DiagramNode.get(n) for n in stmt.nodes]
                for node1, node2 in zip(nodes[:-1], nodes[1:]):
                    route = Route(node1, node2)
                    route.set_attributes(stmt.attrs)
                    self.diagram.routes.append(route)

            elif isinstance(stmt, parser.Attr):
                self.diagram.set_attribute(stmt)

            elif isinstance(stmt, parser.Extension):
                if stmt.type == 'class':
                    name = unquote(stmt.name)
                    Diagram.classes[name] = stmt
                elif stmt.type == 'plugin':
                    self.diagram.set_plugin(stmt.name, stmt.attrs)

            elif isinstance(stmt, parser.Statements):
                self.instantiate(network, group, stmt)

        return network


class DiagramLayoutManager:
    def __init__(self, diagram):
        self.diagram = diagram

        self.coordinates = []

    def run(self):
        self.do_layout()
        self.diagram.fixiate()

    def do_layout(self):
        self.layout_nodes()
        self.set_network_size()

    def layout_nodes(self, group=None):
        networks = self.diagram.networks

        if group:
            nodes = (n for n in self.diagram.nodes if n.group == group)
        else:
            nodes = self.diagram.nodes

        for node in nodes:
            if node.layouted:
                continue

            joined = [g for g in node.networks if g.hidden is False]
            y1 = min(networks.index(g) for g in node.networks)
            if joined:
                y2 = max(networks.index(g) for g in joined)
            else:
                y2 = y1

            if node.group and node.group != self.diagram and group:
                starts = min(n.xy.x for n in group.nodes if n.layouted)
            else:
                nw = [n for n in node.networks if n.xy.y == y1][0]
                nodes = [n for n in self.diagram.nodes if nw in n.networks]
                layouted = [n for n in nodes if n.xy.x > 0]

                starts = 0
                if layouted:
                    layouted.sort(key=lambda a: a.xy.x)
                    basenode = layouted[0]
                    commonnw = set(basenode.networks) & set(node.networks)

                    if basenode.xy.y == y1:
                        starts = basenode.xy.x + 1
                    elif commonnw and list(commonnw)[0].hidden is True:
                        starts = basenode.xy.x
                    else:
                        starts = basenode.xy.x + 1 - len(nodes)

                if starts < 0:
                    starts = 0

            for x in range(starts, len(self.diagram.nodes)):
                points = [XY(x, y) for y in range(y1, y2 + 1)]
                if not set(points) & set(self.coordinates):
                    node.xy = XY(x, y1)
                    node.layouted = True
                    self.coordinates += points
                    break

            if node.group and node.group != self.diagram and group is None:
                self.layout_nodes(node.group)

        if group:
            self.set_coordinates(group)

    def set_coordinates(self, group):
        self.set_group_size(group)

        xy = group.xy
        for i in range(xy.x, xy.x + group.colwidth):
            for j in range(xy.y, xy.y + group.colheight):
                self.coordinates.append(XY(i, j))

    def set_network_size(self):
        for network in self.diagram.networks:
            nodes = [n for n in self.diagram.nodes if network in n.networks]
            nodes.sort(key=lambda a: a.xy.x)

            x0 = min(n.xy.x for n in nodes)
            network.xy = XY(x0, network.xy.y)

            x1 = max(n.xy.x for n in nodes)
            network.colwidth = x1 - x0 + 1

    def set_group_size(self, group):
        nodes = list(group.nodes)
        nodes.sort(key=lambda a: a.xy.x)

        x0 = min(n.xy.x for n in nodes)
        y0 = min(n.xy.y for n in nodes)
        group.xy = XY(x0, y0)

        x1 = max(n.xy.x for n in nodes)
        y1 = max(n.xy.y for n in nodes)
        group.colwidth = x1 - x0 + 1
        group.colheight = y1 - y0 + 1


class ScreenNodeBuilder:
    @classmethod
    def build(cls, tree):
        DiagramNode.clear()
        DiagramEdge.clear()
        NodeGroup.clear()
        Network.clear()

        diagram = DiagramTreeBuilder().build(tree)
        DiagramLayoutManager(diagram).run()
        diagram = cls.update_network_status(diagram)

        return diagram

    @classmethod
    def update_network_status(cls, diagram):
        for node in diagram.nodes:
            above = [nw for nw in node.networks if nw.xy.y <= node.xy.y]
            if len(above) > 1 and [nw for nw in above if nw.hidden]:
                for nw in above:
                    nw.hidden = False

            below = [nw for nw in node.networks if nw.xy.y > node.xy.y]
            if len(below) > 1 and [nw for nw in below if nw.hidden]:
                for nw in below:
                    nw.hidden = False

        return diagram
