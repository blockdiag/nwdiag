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

import math
import blockdiag.DiagramMetrix
from blockdiag import elements
from blockdiag.utils.namedtuple import namedtuple
from blockdiag.utils.XY import XY


class DiagramMetrix(blockdiag.DiagramMetrix.DiagramMetrix):
    def __init__(self, diagram, **kwargs):
        super(DiagramMetrix, self).__init__(diagram, **kwargs)

        self.setdefault('networks', diagram.networks)

        if diagram.page_padding is None and kwargs.get('pagePadding') is None:
            top_padding = self['spanHeight']
            bottom_padding = self['spanHeight'] / 3
            right_padding = (self['nodeWidth'] / 2 + self['spanWidth'])
            left_padding = (self['nodeWidth'] + self['spanWidth']) * 3 / 4

            margin = self['cellSize'] * 6
            self['pagePadding'] = [top_padding + margin,
                                   right_padding,
                                   bottom_padding + margin,
                                   left_padding + margin]

        self['pageMargin'] = XY(0, 0)

    def originalMetrix(self):
        kwargs = {}
        for key in self:
            kwargs[key] = self[key]
        kwargs['scale_ratio'] = 1

        return DiagramMetrix(self, **kwargs)

    def node(self, node):
        metrix = super(DiagramMetrix, self).node(node)
        return NodeMetrix(node, metrix)

    def cell(self, node):
        if isinstance(node, elements.NodeGroup):
            metrix = GroupMetrix(node, self)
        else:
            metrix = super(DiagramMetrix, self).cell(node)
        return metrix

    def network(self, network):
        return NetworkMetrix(network, self)


class NetworkMetrix(blockdiag.DiagramMetrix.NodeMetrix):
    @property
    def trunkline(self):
        x0 = self.left().x
        x1 = self.right().x
        y = self.top().y

        return [XY(x0, y), XY(x1, y)]

    def top(self):
        pt = super(NetworkMetrix, self).top()
        return XY(pt.x, pt.y - self.metrix.spanHeight / 2)

    def left(self):
        pt = super(NetworkMetrix, self).left()
        return XY(pt.x - self.metrix.spanWidth / 2, pt.y)

    def right(self):
        pt = super(NetworkMetrix, self).right()
        return XY(pt.x + self.metrix.spanWidth / 2, pt.y)

    @property
    def textbox(self):
        x = self.left().x
        y = self.top().y

        width = self.metrix.nodeWidth * 3 / 2
        height = self.metrix.nodeHeight

        return (x - width, y - height / 2, x, y + height / 2)


class NodeMetrix(object):
    def __init__(self, node, metrix):
        self.node = node
        self.metrix = metrix

    def top(self):
        return self.metrix.top()

    def bottom(self):
        return self.metrix.bottom()

    @property
    def connectors(self):
        m = self.metrix.metrix

        above = [n for n in self.node.networks if n.xy.y <= self.node.xy.y]
        above.sort(lambda a, b: -cmp(a.xy.y, b.xy.y))

        bottom = [n for n in self.node.networks if n.xy.y > self.node.xy.y]
        bottom.sort(lambda a, b: cmp(a.xy.y, b.xy.y))

        Connector = namedtuple('Connector', 'network line textbox')

        for networks in [above, bottom]:
            for network in networks:
                if network.xy.y <= self.node.xy.y:
                    x, y2 = self.top()
                    y1 = m.network(network).top().y
                else:
                    x, y1 = self.bottom()
                    y2 = m.network(network).top().y

                if len(networks) == 1:
                    dx = 0
                else:
                    pos = networks.index(network)
                    base_x = (len(networks) - 1) / 2.0 - pos
                    dx = int(math.floor(base_x * m.cellSize * 2))

                width = m.nodeWidth + m.spanWidth
                textbox = [x + dx - m.cellSize, y2 - m.spanHeight / 2,
                           x + width - m.cellSize * 2, y2]
                line = [XY(x + dx, y1), XY(x + dx, y2)]

                yield Connector(network, line, textbox)


class GroupMetrix(blockdiag.DiagramMetrix.NodeMetrix):
    def __init__(self, node, metrix):
        super(GroupMetrix, self).__init__(node, metrix)

        self.is_root_group = False
        if node.nodes:
            networks = node.nodes[0].networks[:]
            networks.sort(lambda a, b: cmp(a.xy.y, b.xy.y))
            network = min(networks)
            if self.top().x == metrix.network(network).top().x:
                self.is_root_group = True

    def groupLabelBox(self):
        box = super(GroupMetrix, self).groupLabelBox()
        span = self.metrix.cellSize
        box = (box[0], box[1] + span, box[2], box[3] + span)

        if self.is_root_group:
            width = (self.metrix.nodeWidth + self.metrix.spanWidth) / 2
            box = (box[0] + width, box[1], box[2] + width, box[3])

        return box

    def marginBox(self):
        box = super(GroupMetrix, self).box()
        margin_x = self.metrix.spanHeight / 2 - self.metrix.cellSize
        margin_y = self.metrix.cellSize
        return (box[0] - margin_y, box[1] - margin_x,
                box[2] + margin_y, box[3] + margin_x)
