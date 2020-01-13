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

from packetdiag.metrics import DiagramMetrics


class DiagramDraw(blockdiag.drawer.DiagramDraw):
    def create_metrics(self, *args, **kwargs):
        return DiagramMetrics(*args, **kwargs)

    def _draw_background(self):
        # do not call blockdiag.DiagramDraw#_draw_background()

        scale_interval = self.diagram.scale_interval
        if scale_interval is None:
            scale_interval = self.diagram.colwidth / 2

        # draw measure lines and labels
        font = self.metrics.font_for(None)
        for i in range(self.diagram.colwidth + 1):
            line = self.metrics.measure_line(i)
            self.drawer.line(line, fill=self.diagram.linecolor)

            if (i % scale_interval) == 0:
                box = self.metrics.measure_label(i)

                if self.diagram.scale_direction == "left_to_right":
                    label = str(i)
                else:
                    label = str(self.diagram.colwidth - i)

                self.drawer.textarea(box, label, font,
                                     fill=self.diagram.textcolor)
