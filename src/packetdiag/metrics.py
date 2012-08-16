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
from blockdiag.utils.collections import defaultdict
import elements


class DiagramMetrics(blockdiag.DiagramMetrics.DiagramMetrics):
    def __init__(self, diagram, **kwargs):
        span_height = self.span_height
        span_width = self.span_width
        self.span_height = 0
        self.span_width = 0
        self.node_width = self.cellsize * 6
        super(DiagramMetrics, self).__init__(diagram, **kwargs)

        # reset node_width FORCE
        self.spreadsheet.node_width = defaultdict(lambda: self.node_width)

        self.spreadsheet.set_span_height(0, span_height)
        self.spreadsheet.set_span_height(diagram.colheight, span_height)
        self.spreadsheet.set_span_width(0, span_width)
        self.spreadsheet.set_span_width(diagram.colwidth, span_width)
