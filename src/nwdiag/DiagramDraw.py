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
from blockdiag.DiagramMetrics import DiagramMetrics


class DiagramDraw(blockdiag.DiagramDraw.DiagramDraw):
    def __init__(self, format, diagram, filename=None, **kwargs):
        super(DiagramDraw, self).__init__(format, diagram, filename, **kwargs)
        self.drawer.forward = 'vertical'
        self.drawer.jump_radius = self.metrics.jump_radius
        self.drawer.jump_shift = self.metrics.jump_shift

    @property
    def groups(self):
        return self.diagram.groups

    def pagesize(self, scaled=False):
        # FIXME: force int'ize
        xy = super(DiagramDraw, self).pagesize(scaled)
        return XY(int(xy.x), int(xy.y))

    def _draw_background(self):
        super(DiagramDraw, self)._draw_background()
        self._draw_trunklines_shadow()

    def _draw_trunklines_shadow(self):
        xdiff = self.metrics.shadow_offset.x
        ydiff = self.metrics.shadow_offset.y

        metrics = self.metrics.originalMetrics()
        for network in self.diagram.networks:
            if network.hidden == False:
                self.trunkline(network, shadow=True)

    def _draw_trunklines(self):
        metrics = self.metrics
        for network in self.diagram.networks:
            if network.hidden == False:
                self.trunkline(network)

                # FIXME: first network links to global network
                if network == self.diagram.networks[0]:
                    r = metrics.trunk_diameter / 2

                    pt = metrics.network(network).top
                    pt0 = XY(pt.x, pt.y - metrics.span_height * 2 / 3)
                    pt1 = XY(pt.x, pt.y - r)

                    self.drawer.line([pt0, pt1], fill=network.linecolor)

    def trunkline(self, network, shadow=False):
        if shadow:
            metrics = self.metrics.originalMetrics()
        else:
            metrics = self.metrics

        m = metrics.network(network)
        r = metrics.trunk_diameter / 2

        pt1, pt2 = m.trunkline
        box = (pt1.x, pt1.y - r, pt2.x, pt2.y + r)

        if shadow:
            xdiff = self.metrics.shadow_offset.x
            ydiff = self.metrics.shadow_offset.y / 2

            box = (pt1.x + xdiff, pt1.y - r + ydiff,
                   pt2.x + xdiff, pt2.y + r + ydiff)

        if self.format == 'SVG':
            from blockdiag.imagedraw.simplesvg import pathdata

            path = pathdata(box[0], box[1])
            path.line(box[2], box[1])
            path.ellarc(r / 2, r, 0, 0, 1, box[2], box[3])
            path.line(box[0], box[3])
            path.ellarc(r / 2, r, 0, 0, 1, box[0], box[1])

            if shadow:
                self.drawer.path(path, fill=self.shadow, filter='blur')
            else:
                self.drawer.path(path, fill=network.color,
                                 outline=network.linecolor)

                path = pathdata(box[2], box[3])
                path.ellarc(r / 2, r, 0, 0, 1, box[2], box[1])
                self.drawer.path(path, fill='none', outline=network.linecolor)

                # for edge jumping
                line = (XY(box[0], box[1]), XY(box[2], box[1]))
                self.drawer.line(line, fill='none', jump=True)
        else:
            lsection = (box[0] - r / 2, box[1], box[0] + r / 2, box[3])
            rsection = (box[2] - r / 2, box[1], box[2] + r / 2, box[3])

            if shadow:
                color = self.shadow
            else:
                color = network.color

            # fill background
            self.drawer.rectangle(box, outline=color, fill=color)
            self.drawer.ellipse(lsection, outline=color, fill=color)
            self.drawer.ellipse(rsection, outline=color, fill=color)

            if not shadow:
                upper = (XY(box[0], box[1]), XY(box[2], box[1]))
                self.drawer.line(upper,
                                 fill=network.linecolor, jump=True)

                bottom = (XY(box[0], box[3]), XY(box[2], box[3]))
                self.drawer.line(bottom,
                                 fill=network.linecolor, jump=True)

                self.drawer.arc(lsection, 90, 270, fill=network.linecolor)
                self.drawer.ellipse(rsection, outline=network.linecolor,
                                    fill=network.color)

    def _draw_elements(self):
        self._draw_trunklines()
        self._draw_trunkline_labels()
        super(DiagramDraw, self)._draw_elements()

    def _draw_trunkline_labels(self):
        for network in self.diagram.networks:
            if network.display_label:
                m = self.metrics.network(network)
                self.drawer.textarea(m.textbox, network.display_label,
                                     fill=self.diagram.textcolor,
                                     halign="right", font=self.font,
                                     fontsize=self.metrics.fontsize)

    def node(self, node, **kwargs):
        m = self.metrics

        for connector in m.node(node).connectors:
            self.draw_connector(connector)

            if connector.network in node.address:
                label = node.address[connector.network]
                self.drawer.textarea(connector.textbox, label,
                                     fill=node.textcolor,
                                     halign="left", font=self.font,
                                     fontsize=self.metrics.fontsize)

        super(DiagramDraw, self).node(node, **kwargs)

    def draw_connector(self, connector):
        m = self.metrics
        self.drawer.line(connector.line,
                         fill=connector.network.linecolor, jump=True)

    def group_label(self, group):
        if group.label:
            m = self.metrics.cell(group)
            self.drawer.textarea(m.grouplabelbox, group.label, valign='top',
                                 fill=group.textcolor, font=self.font,
                                 fontsize=self.metrics.fontsize)


from DiagramMetrics import DiagramMetrics
DiagramDraw.set_metrics_class(DiagramMetrics)
