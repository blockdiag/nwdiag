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

        for connector in m.node(node).connectors:
            for i in range(node.xy.y + 1, connector.network.xy.y):
                networks = (n for n in self.diagram.networks if n.xy.y == i)
                for nw in networks:
                    if nw.xy.x <= node.xy.x <= nw.xy.x + nw.width:
                        connector.jumps.append(nw)

            self.draw_connector(connector)

            if connector.network in node.address:
                label = node.address[connector.network]
                self.drawer.textarea(connector.textbox, label, fill=self.fill,
                                     halign="left", font=self.font,
                                     fontsize=self.metrix.fontSize)

        super(DiagramDraw, self).node(node, **kwargs)

    def draw_connector(self, connector):
        m = self.metrix

        if connector.jumps:
            pt1, pt2 = connector.line
            lines = [pt1]
            for nw in connector.jumps:
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
            self.drawer.line(connector.line, fill=self.fill)


from DiagramMetrix import DiagramMetrix
DiagramDraw.set_metrix_class(DiagramMetrix)
