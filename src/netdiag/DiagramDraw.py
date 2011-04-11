#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import blockdiag.DiagramDraw
from blockdiag.utils.XY import XY
from blockdiag import noderenderer
from blockdiag.DiagramMetrix import DiagramMetrix


class DiagramDraw(blockdiag.DiagramDraw.DiagramDraw):
    @property
    def edges(self):
        return []

    def _draw_background(self):
        metrix = self.metrix.originalMetrix()

        # Drop node shadows.
        for node in self.nodes:
            r = noderenderer.get(node.shape)

            shape = r(node, metrix)
            shape.render(self.drawer, self.format,
                         fill=self.shadow, shadow=True)

        # Smoothing back-ground images.
        if self.format == 'PNG':
            self.drawer = self.drawer.smoothCanvas()

        self._draw_trunklines()

    def _draw_trunklines(self):
        m = self.metrix.originalMetrix()

        for network in self.diagram.nodes:
            y = m.node(network.nodes[0]).top().y - m.spanHeight / 3
            x0 = m.node(network.nodes[0]).left().x - m.spanWidth
            x1 = m.node(network.nodes[-1]).right().x + m.spanWidth / 2

            self.drawer.line([XY(x0, y), XY(x1, y)], fill=self.fill)

        for link in self.diagram.edges:
            node1 = m.node(link.node1.nodes[0])
            node2 = m.node(link.node2.nodes[0])

            x = node2.left().x - m.spanWidth / 2 + m.cellSize
            y0 = node1.top().y - m.spanHeight / 3
            y1 = node2.top().y - m.spanHeight / 3

            self.drawer.line([XY(x, y0), XY(x, y1)], fill=self.fill)

        # FIXME: first network links to global network
        network = self.diagram.nodes[0]
        pt1 = m.node(network.nodes[0]).top()
        pt2 = m.node(network.nodes[0-1]).top()
        x = pt1.x + (pt2.x - pt1.x) / 2
        y0 = pt1.y - m.spanHeight * 2 / 3
        y1 = pt1.y - m.spanHeight / 3
        self.drawer.line([XY(x, y0), XY(x, y1)], fill=self.fill)

    def node(self, node, **kwargs):
        m = self.metrix
        pt0 = m.node(node).top()
        pt1 = XY(pt0.x, pt0.y - m.spanHeight / 3)
        self.drawer.line([pt1, pt0], fill=self.fill)

        if node.address:
            label = node.address
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

        box = m.cell(group.nodes[0]).box()
        box = [box[0] - m.nodeWidth - m.spanWidth,
               box[1] - m.nodeHeight / 2 - m.spanHeight / 3,
               box[2] - m.nodeWidth - m.spanWidth,
               box[3] - m.nodeHeight / 2 - m.spanHeight / 3]
        self.drawer.textarea(box, label, fill=self.fill, halign="right",
                             font=self.font, fontsize=self.metrix.fontSize)
