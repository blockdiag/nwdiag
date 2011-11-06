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

import re
import sys
import blockdiag.elements
from blockdiag.elements import *
from blockdiag.utils import images, XY


class RackItem(blockdiag.elements.DiagramNode):
    def __init__(self, number, label):
        super(RackItem, self).__init__(None)
        self.number = int(number)
        self.label = label
        self.ampere = None
        self.weight = None

    @property
    def display_label(self):
        attrs = []
        if self.colheight > 1:
            attrs.append(u"%dU" % self.colheight)
        if self.ampere:
            attrs.append(u"%.1fA" % self.ampere)
        if self.weight:
            attrs.append(u"%.1fkg" % self.weight)

        if attrs:
            return u"%s\n[%s]" % (self.label, u"/".join(attrs))
        else:
            return self.label

    def set_attribute(self, attr):
        if re.search('^\d+U$', attr.name):
            self.colheight = int(attr.name[:-1])
        elif re.search('^\d+(\.[0-9]+)?A$', attr.name):
            self.ampere = float(attr.name[:-1])
        elif re.search('^\d+(\.[0-9]+)?kg$', attr.name):
            self.weight = float(attr.name[:-2])
        else:
            return super(RackItem, self).set_attribute(attr)

    def set_height(self, value):
        self.colheight = int(value)


class Diagram(blockdiag.elements.Diagram):
    def __init__(self):
        super(Diagram, self).__init__()

        self.rackheight = 42

    def set_rackheight(self, value):
        self.rackheight = int(value)
