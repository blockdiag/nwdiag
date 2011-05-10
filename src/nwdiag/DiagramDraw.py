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

import sys
import math
import blockdiag.DiagramDraw
from blockdiag.utils.XY import XY
from blockdiag import noderenderer
from blockdiag.DiagramMetrix import DiagramMetrix


class DiagramDraw(blockdiag.DiagramDraw.DiagramDraw):
    def pagesize(self, scaled=False):
        # FIXME: force int'ize
        xy = super(DiagramDraw, self).pagesize(scaled)
        return XY(int(xy.x), int(xy.y))

    def _draw_background(self):
        super(DiagramDraw, self)._draw_background()

        self._draw_trunklines()

    def _draw_trunklines(self):
        for network in self.diagram.networks:
            m = self.metrix.network(network)

            self.drawer.line(m.trunkline, fill=self.fill)
            if network.display_label:
                self.drawer.textarea(m.textbox, network.display_label,
                                     fill=self.fill, halign="right",
                                     font=self.font,
                                     fontsize=self.metrix.fontSize)

            # FIXME: first network links to global network
            if network == self.diagram.networks[0]:
                pt1 = m.top()
                pt0 = XY(pt1.x, pt1.y - m.metrix.spanHeight * 2 / 3)

                self.drawer.line([pt0, pt1], fill=self.fill)

    def node(self, node, **kwargs):
        m = self.metrix

        i = 0
        textbox_width = m.nodeWidth + m.spanWidth
        node.networks.sort(lambda a, b: cmp(a.xy.y, b.xy.y))
        for network in node.networks:
            if network.xy.y == node.xy.y:
                x, y2 = m.node(node).top()
                y1 = m.network(network).top().y

                x_shift = 0
                textbox = [x, y1, x + textbox_width, y2]
            else:
                x, y1 = m.node(node).bottom()
                y2 = m.network(network).top().y

                num = len(node.networks) - 2
                x_shift = int(math.floor(num / 2.0 - i)) * m.cellSize * 2

                i += 1

            textbox = [x + x_shift, y2 - m.spanHeight / 2, x + textbox_width, y2]
            x += x_shift

            jumps = []
            for j in range(node.xy.y + 1, network.xy.y):
                crosses = (n for n in self.diagram.networks if n.xy.y == j)
                for nw in crosses:
                    if nw.xy.x <= node.xy.x <= nw.xy.x + nw.width:
                        jumps.append(nw)

            self.draw_connectors([XY(x, y1), XY(x, y2)], jumps)

            if network in node.address:
                label = node.address[network]
                self.drawer.textarea(textbox, label, fill=self.fill,
                                     halign="left", font=self.font,
                                     fontsize=self.metrix.fontSize)

        super(DiagramDraw, self).node(node, **kwargs)

    def draw_connectors(self, line, jumps):
        m = self.metrix

        if jumps:
            pt1, pt2 = line
            lines = [pt1]
            for nw in jumps:
                pt = m.cell(nw).top().y - m.spanHeight / 2
                r = m.cellSize / 2

                lines.append(XY(pt1.x, pt - r))
                lines.append(XY(pt1.x, pt + r))

                box = [pt1.x - r, pt - r, pt1.x + r, pt + r]
                self.drawer.arc(box, 270, 90, fill=self.fill)

            lines.append(pt2)

            for j, point in enumerate(lines[::2]):
                self.drawer.line([point, lines[j * 2 + 1]], fill=self.fill)
        else:
            self.drawer.line(line, fill=self.fill)


from DiagramMetrix import DiagramMetrix
DiagramDraw.set_metrix_class(DiagramMetrix)
