#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        m = self.metrix

        for network in self.diagram.networks:
            nodes = [n for n in self.diagram.nodes  if network in n.networks]
            nodes.sort(lambda a, b: cmp(a.xy.x, b.xy.x))

            cell = m.cell(network)
            y = cell.top().y - m.spanHeight / 2
            x0 = cell.left().x - m.spanWidth / 2
            x1 = cell.right().x + m.spanWidth / 2

            self.drawer.line([XY(x0, y), XY(x1, y)], fill=self.fill)

            self.network_label(network)

            # FIXME: first network links to global network
            if network == self.diagram.networks[0]:
                x = x0 + (x1 - x0) / 2
                y0 = y - m.spanHeight * 2 / 3

                self.drawer.line([XY(x, y0), XY(x, y)], fill=self.fill)

    def node(self, node, **kwargs):
        m = self.metrix
        pt0 = m.node(node).top()
        pt1 = XY(pt0.x, pt0.y - m.spanHeight / 3)

        i = 0
        for network in node.networks:
            if network.xy.y == node.xy.y:
                x, y = m.cell(node).top()

                y0 = m.cell(network).top().y - m.spanHeight / 2
                textbox = [x, y0, x + m.nodeWidth / 2, y]
            else:
                x, y = m.cell(node).bottom()
                x -= i * m.cellSize * 2

                y0 = m.cell(network).top().y - m.spanHeight / 2
                textbox = [x, y0 - m.spanHeight / 2, x + m.nodeWidth / 2, y0]

                i += 1

            self.drawer.line([XY(x, y0), XY(x, y)], fill=self.fill)

            if network in node.address:
                label = node.address[network]
                self.drawer.textarea(textbox, label, fill=self.fill,
                                     halign="left", font=self.font,
                                     fontsize=self.metrix.fontSize)

        super(DiagramDraw, self).node(node, **kwargs)

    def network_label(self, network):
        m = self.metrix

        if network.label:
            label = network.label
        else:
            label = network.id

        if network.address:
            if label:
                label += "\n"

            label += network.address

        cell = m.cell(network)
        y = cell.top().y - m.spanHeight / 2
        x = cell.left().x - m.spanWidth / 2

        box = [x - m.nodeWidth * 3 / 2, y - m.nodeHeight / 2,
               x, y + m.nodeHeight / 2]
        self.drawer.textarea(box, label, fill=self.fill, halign="right",
                             font=self.font, fontsize=self.metrix.fontSize)
