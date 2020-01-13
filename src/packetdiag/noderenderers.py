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

from blockdiag.noderenderer import install_renderer

try:
    from blockdiag.noderenderer.base import NodeShape
except ImportError:
    from blockdiag.noderenderer import NodeShape


class PacketNode(NodeShape):
    def render_shape(self, drawer, _, **kwargs):
        # draw outline
        box = self.metrics.cell(self.node).box
        if kwargs.get('shadow'):
            pass
        else:
            drawer.rectangle(box, fill=self.node.color,
                             outline=self.node.color)
            if self.node.background:
                drawer.loadImage(self.node.background, self.textbox)

            self.line(drawer, box.topleft, box.topright, False)
            self.line(drawer, box.topright, box.bottomright,
                      self.node.separated_right)
            self.line(drawer, box.bottomright, box.bottomleft, False)
            self.line(drawer, box.bottomleft, box.topleft,
                      self.node.separated_left)

    def line(self, drawer, _from, _to, is_dashed):
        if is_dashed:
            style = 'dashed'
        else:
            style = self.node.style

        drawer.line((_from, _to), fill=self.node.linecolor, style=style)


def setup(self):
    install_renderer('_packet_node', PacketNode)
