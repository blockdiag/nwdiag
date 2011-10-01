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
    def __init__(self, format, diagram, filename=None, **kwargs):
        super(DiagramDraw, self).__init__(format, diagram, filename, **kwargs)
        self.drawer.forward = 'vertical'
        self.drawer.jump_radius = self.metrix.jump_radius

    @property
    def groups(self):
        return self.diagram.groups

    def pagesize(self, scaled=False):
        # FIXME: force int'ize
        xy = super(DiagramDraw, self).pagesize(scaled)
        return XY(int(xy.x), int(xy.y))

    def _draw_background(self):
        super(DiagramDraw, self)._draw_background()

        self._draw_trunklines()

    def _draw_trunklines(self):
        metrix = self.metrix.originalMetrix()
        for network in self.diagram.networks:
            if network.hidden == False:
                m = metrix.network(network)
                r = metrix.trunk_diameter / 2

                pt1, pt2 = m.trunkline
                box = (pt1.x, pt1.y - r, pt2.x, pt2.y + r)
                self.drawer.rectangle(box, outline=network.color,
                                      fill=network.color)

                upper = (XY(pt1.x, pt1.y - r), XY(pt2.x, pt2.y - r))
                self.drawer.line(upper,
                                 fill=network.linecolor, jump=True)

                bottom = (XY(pt1.x, pt1.y + r), XY(pt2.x, pt2.y + r))
                self.drawer.line(bottom,
                                 fill=network.linecolor, jump=True)

                arcbox = (upper[0].x - r / 2, upper[0].y,
                          bottom[0].x + r / 2, bottom[0].y)
                self.drawer.arc(arcbox, 90, 270, fill=network.linecolor)

                ellbox = (upper[1].x - r / 2, upper[1].y,
                          bottom[1].x + r / 2, bottom[1].y)
                self.drawer.ellipse(ellbox, outline=network.linecolor,
                                    fill=network.color)

                # FIXME: first network links to global network
                if network == self.diagram.networks[0]:
                    pt = m.top()
                    pt0 = XY(pt.x, pt.y - m.metrix.spanHeight * 2 / 3)
                    pt1 = XY(pt.x, pt.y - r)

                    self.drawer.line([pt0, pt1], fill=network.linecolor)

    def draw(self):
        super(DiagramDraw, self).draw()

        self._draw_trunkline_labels()

    def _draw_trunkline_labels(self):
        for network in self.diagram.networks:
            if network.display_label:
                m = self.metrix.network(network)
                self.drawer.textarea(m.textbox, network.display_label,
                                     fill=self.diagram.textcolor,
                                     halign="right", font=self.font,
                                     fontsize=self.metrix.fontSize)

    def node(self, node, **kwargs):
        m = self.metrix

        for connector in m.node(node).connectors:
            self.draw_connector(connector)

            if connector.network in node.address:
                label = node.address[connector.network]
                self.drawer.textarea(connector.textbox, label,
                                     fill=node.textcolor,
                                     halign="left", font=self.font,
                                     fontsize=self.metrix.fontSize)

        super(DiagramDraw, self).node(node, **kwargs)

    def draw_connector(self, connector):
        m = self.metrix
        self.drawer.line(connector.line,
                         fill=connector.network.linecolor, jump=True)

    def group_label(self, group):
        if group.label:
            m = self.metrix.cell(group)
            self.drawer.textarea(m.groupLabelBox(), group.label, valign='top',
                                 fill=group.textcolor, font=self.font,
                                 fontsize=self.metrix.fontSize)


from DiagramMetrix import DiagramMetrix
DiagramDraw.set_metrix_class(DiagramMetrix)
