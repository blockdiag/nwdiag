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
from blockdiag.utils.namedtuple import namedtuple
from blockdiag.utils.XY import XY


class DiagramMetrix(blockdiag.DiagramMetrix.DiagramMetrix):
    def __init__(self, diagram, **kwargs):
        super(DiagramMetrix, self).__init__(diagram, **kwargs)

        self.setdefault('networks', diagram.networks)

        if diagram.page_padding is None:
            top_padding = self['spanHeight'] / 2
            left_padding = (self['nodeWidth'] + self['spanWidth']) * 3 / 4
            self['pagePadding'] = [top_padding, 0, 0, left_padding]

    def originalMetrix(self):
        kwargs = {}
        for key in self:
            kwargs[key] = self[key]
        kwargs['scale_ratio'] = 1

        return DiagramMetrix(self, **kwargs)

    def node(self, node):
        metrix = super(DiagramMetrix, self).node(node)
        return NodeMetrix(node, metrix)

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

        Connector = namedtuple('Connector', 'network line textbox jumps')

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
                textbox = [x + dx, y2 - m.spanHeight / 2, x + width, y2]
                line = [XY(x + dx, y1), XY(x + dx, y2)]

                yield Connector(network, line, textbox, [])
