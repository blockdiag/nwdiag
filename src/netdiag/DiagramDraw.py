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
        metrix = self.metrix.originalMetrix()

        self._draw_trunklines()

        # Drop node shadows.
        for node in self.nodes:
            r = noderenderer.get(node.shape)

            shape = r(node, metrix)
            shape.render(self.drawer, self.format,
                         fill=self.shadow, shadow=True)

        # Smoothing back-ground images.
        if self.format == 'PNG':
            self.drawer = self.drawer.smoothCanvas()

    def _draw_trunklines(self):
        m = self.metrix.originalMetrix()

        for network in self.diagram.nodes:
            y = m.node(network.nodes[0]).top().y - m.spanHeight / 3
            x0 = m.node(network.nodes[0]).left().x - m.spanWidth / 2
            x1 = m.node(network.nodes[-1]).right().x + m.spanWidth / 2

            self.drawer.line([XY(x0, y), XY(x1, y)], fill=self.fill)

    def node(self, node, **kwargs):
        m = self.metrix
        pt0 = m.node(node).top()
        pt1 = XY(pt0.x, pt0.y - m.spanHeight / 3)
        self.drawer.line([pt1, pt0], fill=self.fill)

        super(DiagramDraw, self).node(node, **kwargs)

    def group_label(self, group):
        m = self.metrix.cell(group)

        if self.format == 'SVG' and group.href:
            drawer = self.drawer.link(group.href)
        else:
            drawer = self.drawer

        if group.label and not group.separated:
            drawer.textarea(m.groupLabelBox(), group.label, fill=self.fill,
                            font=self.font, fontsize=self.metrix.fontSize)
        elif group.label:
            drawer.textarea(m.coreBox(), group.label, fill=self.fill,
                            font=self.font, fontsize=self.metrix.fontSize)
