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
        pt0 = m.node(node).top()
        pt1 = XY(pt0.x, pt0.y - m.spanHeight / 3)

        i = 0
        textbox_width = m.nodeWidth + m.spanWidth
        node.networks.sort(lambda a, b: cmp(a.xy.y, b.xy.y))
        for network in node.networks:
            jumps = []
            if network.xy.y == node.xy.y:
                x, y = m.cell(node).top()

                y0 = m.cell(network).top().y - m.spanHeight / 2
                textbox = [x, y0, x + textbox_width, y]
            else:
                x, y = m.cell(node).bottom()
                num = len(node.networks) - 2
                x_shift = int(math.floor(num / 2.0 - i)) * m.cellSize * 2
                x += x_shift

                y0 = m.cell(network).top().y - m.spanHeight / 2
                textbox = [x, y0 - m.spanHeight / 2,
                           x + textbox_width - x_shift, y0]

                i += 1

                for j in range(node.xy.y + 1, network.xy.y):
                    crosses = (n for n in self.diagram.networks if n.xy.y == j)
                    for nw in crosses:
                        if nw.xy.x <= node.xy.x <= nw.xy.x + nw.width:
                            jumps.append(nw)

            if jumps:
                lines = [XY(x, y)]
                for nw in jumps:
                    pt = m.cell(nw).top().y - m.spanHeight / 2
                    r = m.cellSize / 2

                    lines.append(XY(x, pt - r))
                    lines.append(XY(x, pt + r))

                    box = [x - r, pt - r, x + r, pt + r]
                    self.drawer.arc(box, 270, 90, fill=self.fill)

                lines.append(XY(x, y0))

                for j, point in enumerate(lines[::2]):
                    self.drawer.line([point, lines[j * 2 + 1]], fill=self.fill)
            else:
                self.drawer.line([XY(x, y0), XY(x, y)], fill=self.fill)

            if network in node.address:
                label = node.address[network]
                self.drawer.textarea(textbox, label, fill=self.fill,
                                     halign="left", font=self.font,
                                     fontsize=self.metrix.fontSize)

        super(DiagramDraw, self).node(node, **kwargs)


from DiagramMetrix import DiagramMetrix
DiagramDraw.set_metrix_class(DiagramMetrix)
