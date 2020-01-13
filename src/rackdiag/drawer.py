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

import blockdiag.drawer
from blockdiag.utils import Box

from rackdiag.metrics import DiagramMetrics


class DiagramDraw(blockdiag.drawer.DiagramDraw):
    def create_metrics(self, *args, **kwargs):
        return DiagramMetrics(*args, **kwargs)

    def _draw_elements(self, **kwargs):
        default_font = self.metrics.font_for(self.diagram)

        for rack in self.diagram.racks:
            frame = self.metrics.cell(rack, use_padding=False).box
            self.drawer.rectangle(frame, fill='white',
                                  outline=self.diagram.linecolor)

            for i in range(rack.colheight):
                box = self.metrics.racknumber(rack, i)
                number = "%d" % (i + 1)
                self.drawer.textarea(box, number, default_font, halign='right',
                                     fill=self.diagram.textcolor)

            if rack.display_label:
                box = self.metrics.racklabel(rack)
                self.drawer.textarea(box, rack.display_label,
                                     self.metrics.font_for(rack),
                                     fill=rack.textcolor)

        super(DiagramDraw, self)._draw_elements(**kwargs)

    def _draw_background(self):
        # do not draw shadow of nodes on super()
        self.diagram.shadow_style = 'none'
        super(DiagramDraw, self)._draw_background()

        # draw shadow of frame
        dx, dy = self.metrics.shadow_offset
        for rack in self.diagram.racks:
            frame = self.metrics.cell(rack, use_padding=False)
            shadow = Box(frame.x1 + dx, frame.y1 + dy,
                         frame.x2 + dx, frame.y2 + dy)
            self.drawer.rectangle(shadow, fill=self.shadow, filter='blur')

    def node(self, node, **kwargs):
        label, node.label = node.label, node.display_label
        super(DiagramDraw, self).node(node, **kwargs)
        node.label = label
