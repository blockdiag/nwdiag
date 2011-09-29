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
                self.drawer.line(m.trunkline,
                                 fill=self.diagram.linecolor, jump=True)

                # FIXME: first network links to global network
                if network == self.diagram.networks[0]:
                    pt1 = m.top()
                    pt0 = XY(pt1.x, pt1.y - m.metrix.spanHeight * 2 / 3)

                    self.drawer.line([pt0, pt1], fill=self.diagram.linecolor)

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
                         fill=self.diagram.linecolor, jump=True)

    def group_label(self, group):
        if group.label:
            m = self.metrix.cell(group)
            self.drawer.textarea(m.groupLabelBox(), group.label, valign='top',
                                 fill=group.textcolor, font=self.font,
                                 fontsize=self.metrix.fontSize)


from DiagramMetrix import DiagramMetrix
DiagramDraw.set_metrix_class(DiagramMetrix)
