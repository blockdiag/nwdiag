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
from blockdiag.utils.collections import namedtuple
import elements


class DiagramMetrics(blockdiag.DiagramMetrics.DiagramMetrics):
    def __init__(self, diagram, **kwargs):
        span_height = self.span_height
        self.span_height = 0
        super(DiagramMetrics, self).__init__(diagram, **kwargs)

        self.rackheight = diagram.rackheight
        self.spreadsheet.set_span_height(0, span_height)
        self.spreadsheet.set_span_height(diagram.rackheight, span_height)

    @property
    def frame(self):
        dummy = elements.DiagramNode(None)
        dummy.xy = XY(0, 0)
        dummy.colwidth = 1
        dummy.colheight = self.rackheight - 1
        return self.cell(dummy, use_padding=False)

    def racknumber(self, number):
        dummy = elements.DiagramNode(None)
        dummy.xy = XY(0, self.rackheight - number - 1)
        dummy.colwidth = 1
        dummy.colheight = 1

        box = self.cell(dummy, use_padding=False)
        return Box(0, box[1], box[0], box[3])
