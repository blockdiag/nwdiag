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

from __future__ import division

import blockdiag.drawer
from blockdiag.utils import XY, Box

from nwdiag.metrics import DiagramMetrics


class DiagramDraw(blockdiag.drawer.DiagramDraw):
    def create_metrics(self, *args, **kwargs):
        return DiagramMetrics(*args, **kwargs)

    def __init__(self, _format, diagram, filename=None, **kwargs):
        super(DiagramDraw, self).__init__(_format, diagram, filename, **kwargs)
        self.drawer.set_options(jump_forward='vertical',
                                jump_radius=self.metrics.jump_radius,
                                jump_shift=self.metrics.jump_shift)

    @property
    def groups(self):
        return self.diagram.groups

    def pagesize(self, scaled=False):
        return super(DiagramDraw, self).pagesize(scaled).to_integer_point()

    def _draw_background(self):
        super(DiagramDraw, self)._draw_background()
        self.trunklines_shadow()

    def trunklines_shadow(self):
        for network in self.diagram.networks:
            if network.hidden is False and network.color != 'none':
                self.trunkline(network, shadow=True)

    def trunklines(self):
        metrics = self.metrics
        for network in self.diagram.networks:
            if network.hidden is False:
                self.trunkline(network)

                if (self.diagram.external_connector and
                   (network == self.diagram.networks[0])):
                    r = metrics.trunk_diameter // 2

                    pt = metrics.network(network).top
                    pt0 = XY(pt.x, pt.y - metrics.span_height * 2 // 3)
                    pt1 = XY(pt.x, pt.y - r)

                    self.drawer.line([pt0, pt1], fill=network.linecolor)

    def trunkline(self, network, shadow=False):
        metrics = self.metrics
        m = metrics.network(network)
        r = metrics.trunk_diameter // 2

        pt1, pt2 = m.trunkline
        box = Box(pt1.x, pt1.y - r, pt2.x, pt2.y + r)

        if shadow:
            xdiff = self.metrics.shadow_offset.x
            ydiff = self.metrics.shadow_offset.y // 2

            box = Box(pt1.x + xdiff, pt1.y - r + ydiff,
                      pt2.x + xdiff, pt2.y + r + ydiff)

        if self.format == 'SVG':
            from blockdiag.imagedraw.simplesvg import pathdata

            path = pathdata(box[0], box[1])
            path.line(box[2], box[1])
            path.ellarc(r // 2, r, 0, 0, 1, box[2], box[3])
            path.line(box[0], box[3])
            path.ellarc(r // 2, r, 0, 0, 1, box[0], box[1])

            if shadow:
                self.drawer.path(path, fill=self.shadow, filter='blur')
            else:
                self.drawer.path(path, fill=network.color,
                                 outline=network.linecolor)

                path = pathdata(box[2], box[3])
                path.ellarc(r // 2, r, 0, 0, 1, box[2], box[1])
                self.drawer.path(path, fill='none', outline=network.linecolor)

                # for edge jumping
                line = (XY(box[0], box[1]), XY(box[2], box[1]))
                self.drawer.line(line, fill='none', jump=True)
        else:
            lsection = Box(box[0] - r // 2, box[1], box[0] + r // 2, box[3])
            rsection = Box(box[2] - r // 2, box[1], box[2] + r // 2, box[3])

            if shadow:
                color = self.shadow
                _filter = 'blur'
            else:
                color = network.color
                _filter = None

            # fill background
            self.drawer.rectangle(box, outline=color,
                                  fill=color, filter=_filter)
            self.drawer.ellipse(lsection, outline=color,
                                fill=color, filter=_filter)
            self.drawer.ellipse(rsection, outline=color,
                                fill=color, filter=_filter)

            if not shadow:
                upper = (XY(box[0], box[1]), XY(box[2], box[1]))
                self.drawer.line(upper, fill=network.linecolor, jump=True)

                bottom = (XY(box[0], box[3]), XY(box[2], box[3]))
                self.drawer.line(bottom, fill=network.linecolor, jump=True)

                self.drawer.arc(lsection, 90, 270, fill=network.linecolor)
                self.drawer.ellipse(rsection, outline=network.linecolor,
                                    fill=network.color)

    def _draw_elements(self):
        self.trunklines()

        for network in self.diagram.networks:
            self.trunkline_label(network)

        super(DiagramDraw, self)._draw_elements()

    def trunkline_label(self, network):
        if network.display_label:
            m = self.metrics.network(network)
            self.drawer.textarea(m.textbox, network.display_label,
                                 self.metrics.font_for(network),
                                 fill=network.textcolor, halign="right")

    def node(self, node, **kwargs):
        m = self.metrics

        for connector in m.node(node).connectors:
            self.draw_connector(connector)
            if hasattr(connector, 'subject'):
                network = connector.subject.network
            else:
                network = connector.network

            if network in node.address:
                label = node.address[network]
                self.drawer.textarea(connector.textbox, label,
                                     self.metrics.font_for(node),
                                     fill=node.textcolor, halign="left")

        super(DiagramDraw, self).node(node, **kwargs)

    def draw_connector(self, connector):
        if hasattr(connector, 'subject'):
            linecolor = connector.subject.network.linecolor
        else:
            linecolor = connector.network.linecolor
        self.drawer.line(connector.line, fill=linecolor, jump=True)

    def group_label(self, group):
        if group.label:
            m = self.metrics.cell(group)
            self.drawer.textarea(m.grouplabelbox, group.label,
                                 self.metrics.font_for(group),
                                 valign='top', fill=group.textcolor)
