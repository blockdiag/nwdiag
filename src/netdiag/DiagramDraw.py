#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import blockdiag.DiagramDraw
from blockdiag.utils.XY import XY
from blockdiag import noderenderer
from blockdiag.DiagramMetrix import DiagramMetrix


class DiagramDraw(blockdiag.DiagramDraw.DiagramDraw):
    def _draw_background(self):
        super(DiagramDraw, self)._draw_background()

        self._draw_trunklines()

    def _draw_trunklines(self):
        m = self.metrix

        for network in self.diagram.groups:
            nodes = [n for n in self.diagram.nodes  if network in n.groups]
            nodes.sort(lambda a, b: cmp(a.xy.x, b.xy.x))

            cell = m.cell(network)
            y = cell.top().y - m.spanHeight / 2
            x0 = cell.left().x - m.spanWidth / 2
            x1 = cell.right().x + m.spanWidth / 2

            self.drawer.line([XY(x0, y), XY(x1, y)], fill=self.fill)

            self.group_label(network)

            # FIXME: first network links to global network
            if network == self.diagram.groups[0]:
                x = x0 + (x1 - x0) / 2
                y0 = y - m.spanHeight * 2 / 3

                self.drawer.line([XY(x, y0), XY(x, y)], fill=self.fill)

    def node(self, node, **kwargs):
        m = self.metrix
        pt0 = m.node(node).top()
        pt1 = XY(pt0.x, pt0.y - m.spanHeight / 3)

        for network in node.groups:
            if network.xy.y == node.xy.y:
                x, y = m.cell(node).top()
            else:
                x, y = m.cell(node).bottom()

            y0 = m.cell(network).top().y - m.spanHeight / 2
            self.drawer.line([XY(x, y0), XY(x, y)], fill=self.fill)

        if node.address:
            label = node.address[0]
            textbox = [pt1.x, pt1.y, pt0.x + m.nodeWidth, pt0.y]
            self.drawer.textarea(textbox, label, fill=self.fill, halign="left",
                                 font=self.font, fontsize=self.metrix.fontSize)

        super(DiagramDraw, self).node(node, **kwargs)

    def group_label(self, group):
        m = self.metrix

        if group.label:
            label = group.label
        else:
            label = group.id

        if group.address:
            if label:
                label += "\n"

            label += group.address

        cell = m.cell(group)
        y = cell.top().y - m.spanHeight / 2
        x = cell.left().x - m.spanWidth / 2

        box = [x - m.nodeWidth * 3 / 2, y - m.nodeHeight / 2,
               x, y + m.nodeHeight / 2]
        self.drawer.textarea(box, label, fill=self.fill, halign="right",
                             font=self.font, fontsize=self.metrix.fontSize)
