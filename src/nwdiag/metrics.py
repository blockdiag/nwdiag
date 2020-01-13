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

import math
from collections import namedtuple

import blockdiag.metrics
from blockdiag.utils import XY, Box

from nwdiag import elements

cellsize = blockdiag.metrics.DiagramMetrics.cellsize


class DiagramMetrics(blockdiag.metrics.DiagramMetrics):
    node_width = cellsize * 13
    span_width = cellsize * 6
    span_height = cellsize * 13

    def __init__(self, diagram, **kwargs):
        super(DiagramMetrics, self).__init__(diagram, **kwargs)

        self.networks = diagram.networks
        self.trunk_diameter = self.cellsize
        self.jump_shift = self.trunk_diameter // 2
        self.jump_radius = self.trunk_diameter
        self.page_padding = [self.span_height // 2, 0, 0, self.node_width]

        for node in diagram.nodes:
            bottom = [n for n in node.networks if n.xy.y > node.xy.y]
            cnwidth = (len(bottom) + 1) * self.cellsize * 2
            if self.cell(node).width < cnwidth:
                node.width = cnwidth
                self.spreadsheet.set_node_width(node.xy.x, cnwidth)

    def node(self, node):
        n = super(DiagramMetrics, self).cell(node)
        return NodeMetrics(node, self, n.x1, n.y1, n.x2, n.y2)

    def cell(self, node):
        if isinstance(node, elements.Network):
            metrics = super(DiagramMetrics, self).cell(node, use_padding=False)
        elif isinstance(node, elements.NodeGroup):
            n = super(DiagramMetrics, self).cell(node)
            metrics = GroupMetrics(node, self, n.x1, n.y1, n.x2, n.y2)
        else:
            metrics = super(DiagramMetrics, self).cell(node)
        return metrics

    def network(self, network):
        n = self.cell(network)
        return NetworkMetrics(self, n.x1, n.y1, n.x2, n.y2)


class NetworkMetrics(blockdiag.metrics.NodeMetrics):
    @property
    def trunkline(self):
        x0 = self.left.x
        x1 = self.right.x
        y = self.top.y

        return [XY(x0, y), XY(x1, y)]

    @property
    def top(self):
        pt = self.box.top
        return XY(pt.x, pt.y - self.span_height // 2)

    @property
    def left(self):
        pt = self.box.left
        return XY(pt.x - self.span_width // 2, pt.y)

    @property
    def right(self):
        pt = self.box.right
        return XY(pt.x + self.span_width // 2, pt.y)

    @property
    def textbox(self):
        x = self.left.x
        y = self.top.y

        width = self.node_width * 3 // 2
        height = self.node_height

        return Box(x - width, y - height // 2, x, y + height // 2)


class NodeMetrics(blockdiag.metrics.NodeMetrics):
    def __init__(self, node, metrics, x1, y1, x2, y2):
        super(NodeMetrics, self).__init__(metrics, x1, y1, x2, y2)
        self.node = node

    @property
    def connectors(self):
        above = [n for n in self.node.networks if n.xy.y <= self.node.xy.y]
        above.sort(key=lambda a: a.xy.y, reverse=True)

        bottom = [n for n in self.node.networks if n.xy.y > self.node.xy.y]
        bottom.sort(key=lambda a: a.xy.y)

        Connector = namedtuple('Connector', 'network line textbox')

        connectors = []
        for networks in [above, bottom]:
            for network in networks:
                if network.hidden:
                    span = 0
                else:
                    span = self.trunk_diameter // 2

                if network.xy.y <= self.node.xy.y:
                    x, y2 = self.top
                    y1 = self.network(network).top.y + span
                else:
                    x, y1 = self.bottom
                    y2 = self.network(network).top.y - span

                if len(networks) == 1:
                    dx = 0
                else:
                    pos = networks.index(network)
                    base_x = (len(networks) - 1) / 2.0 - pos
                    dx = int(math.floor(base_x * self.cellsize * 2))

                width = self.node_width + self.span_width
                textbox = Box(x + dx + self.cellsize // 2,
                              y2 - self.span_height // 2,
                              x + width - self.cellsize // 2,
                              y2)
                line = [XY(x + dx, y1), XY(x + dx, y2)]

                cn = Connector(network, line, textbox)
                connectors.append(cn)

        return connectors


class GroupMetrics(blockdiag.metrics.NodeMetrics):
    def __init__(self, group, metrics, x1, y1, x2, y2):
        super(GroupMetrics, self).__init__(metrics, x1, y1, x2, y2)

        self.is_root_group = False
        if group.nodes:
            networks = group.nodes[0].networks[:]
            networks.sort(key=lambda a: a.xy.y)
            network = min(networks)
            if self.top.x == metrics.network(network).top.x:
                self.is_root_group = True

    @property
    def grouplabelbox(self):
        box = super(GroupMetrics, self).grouplabelbox
        span = self.cellsize
        box = Box(box[0], box[1] + span, box[2], box[3] + span)

        if self.is_root_group:
            width = (self.node_width + self.span_width) // 2
            box = Box(box[0] + width, box[1], box[2] + width, box[3])

        return box

    @property
    def marginbox(self):
        box = super(GroupMetrics, self).box
        margin_x = self.span_height // 2 - self.cellsize
        margin_y = self.cellsize
        return Box(box[0] - margin_y, box[1] - margin_x,
                   box[2] + margin_y, box[3] + margin_x)
