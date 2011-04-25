#!bin/py
# -*- coding: utf-8 -*-

import re
import sys
import blockdiag.elements
from blockdiag.elements import *
from blockdiag.utils.XY import XY


class Diagram(blockdiag.elements.Diagram):
    def __init__(self):
        super(Diagram, self).__init__()

        self.orientation = 'portrait'
        self.span_height = 120
        self.networks = []

    def set_attributes(self, attrs):
        for attr in attrs:
            value = unquote(attr.value)

            if attr.name == 'default_shape':
                try:
                    noderenderer.get(value)
                    DiagramNode.set_default_shape(value)
                except:
                    msg = "WARNING: unknown node shape: %s\n" % value
                    raise RuntimeError(msg)
            elif attr.name == 'shape_namespace':
                noderenderer.set_default_namespace(value)
            else:
                self.set_attribute(attr)

    def fixiate(self):
        if len(self.nodes) + len(self.networks) > 0:
            nodes = self.nodes + self.networks
            self.width = max(x.xy.x + x.width for x in nodes)
            self.height = max(x.xy.y + x.height for x in nodes)


class DiagramNode(blockdiag.elements.DiagramNode):
    def __init__(self, id):
        super(DiagramNode, self).__init__(id)

        self.address = {}
        self.networks = []

    def set_attributes(self, network, attrs):
        for attr in attrs:
            if attr.name == 'address':
                self.address[network] = unquote(attr.value)
            else:
                self.set_attribute(attr)


class NodeGroup(blockdiag.elements.NodeGroup):
    def __init__(self, id):
        super(NodeGroup, self).__init__(id)

        self.address = None
