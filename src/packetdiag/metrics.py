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

from collections import defaultdict, namedtuple

import blockdiag.metrics
from blockdiag.utils import XY, Box


class DiagramMetrics(blockdiag.metrics.DiagramMetrics):
    def __init__(self, diagram, **kwargs):
        span_height = self.span_height
        span_width = self.span_width
        self.span_height = 0
        self.span_width = 0
        self.node_width = self.cellsize * 3
        self.colwidth = diagram.colwidth
        super(DiagramMetrics, self).__init__(diagram, **kwargs)

        # reset node_width FORCE
        self.spreadsheet.node_width = defaultdict(lambda: self.node_width)

        self.spreadsheet.set_span_height(0, span_height * 2)
        self.spreadsheet.set_span_height(diagram.colheight, span_height)
        self.spreadsheet.set_span_width(0, span_width)
        self.spreadsheet.set_span_width(diagram.colwidth, span_width)

    def measure_line(self, n):
        _Node = namedtuple('Node', 'xy')

        if n == self.colwidth:
            node = _Node(XY(n - 1, 0))
            pt = self.spreadsheet._node_topleft(node, use_padding=False)
            pt = pt.shift(x=self.node_width)
        else:
            node = _Node(XY(n, 0))
            pt = self.spreadsheet._node_topleft(node, use_padding=False)

        if n * 2.0 % self.colwidth == 0:
            return (XY(pt.x, pt.y - self.cellsize * 4), pt)
        elif n * 4.0 % self.colwidth == 0:
            return (XY(pt.x, pt.y - self.cellsize * 4), pt)
        else:
            return (XY(pt.x, pt.y - self.cellsize * 2), pt)

    def measure_label(self, n):
        top, _ = self.measure_line(n)
        cellsize = self.cellsize

        return Box(top.x - cellsize * 4, top.y - cellsize * 3,
                   top.x + cellsize * 4, top.y)
