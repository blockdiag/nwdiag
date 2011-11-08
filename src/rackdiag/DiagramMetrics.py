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

import blockdiag.DiagramMetrics
from blockdiag.utils import Box, XY
from blockdiag.utils.collections import defaultdict, namedtuple
import elements


class DiagramMetrics(blockdiag.DiagramMetrics.DiagramMetrics):
    def __init__(self, diagram, **kwargs):
        span_height = self.span_height
        span_width = self.span_width
        self.span_height = 0
        self.span_width = 0
        super(DiagramMetrics, self).__init__(diagram, **kwargs)

        labels = [r.display_label for r in diagram.racks  if r.display_label]
        if labels:
            labelheight = max(self.textsize(l).y for l in labels) + \
                          self.line_spacing * 2
        else:
            labelheight = 0

        # reset node_width FORCE
        self.spreadsheet.node_width = defaultdict(lambda: self.node_width)

        self.spreadsheet.set_span_height(0, span_height + labelheight)
        self.spreadsheet.set_span_height(diagram.colheight, span_height)
        self.spreadsheet.set_span_width(0, span_width)

        for rack in diagram.racks:
            x = rack.xy.x + rack.colwidth
            self.spreadsheet.set_span_width(x, span_width)

            if rack.colwidth > 1:
                node_width = self.node_width / rack.colwidth
                for i in range(rack.colwidth):
                    self.spreadsheet.set_node_width(rack.xy.x + i, node_width)

                # FIXME: fill node.width to minimum node_width
                #        (bugs in blockdiag-1.0.2)
                for node in rack.nodes:
                    node.width = node_width

    def racklabel(self, rack):
        cell = self.cell(rack)
        textsize = self.textsize(rack.display_label)
        y1 = cell.y1 - textsize.y - self.line_spacing * 2
        return Box(cell.x1, y1, cell.x2, cell.y1)

    def racknumber(self, rack, number):
        if rack.descending:
            y = rack.colheight - number - 1
        else:
            y = number

        dummy = elements.DiagramNode(None)
        dummy.xy = XY(rack.xy.x, y)
        dummy.colwidth = 1
        dummy.colheight = 1

        box = self.cell(dummy, use_padding=False)
        return Box(0, box[1], box[0], box[3])
