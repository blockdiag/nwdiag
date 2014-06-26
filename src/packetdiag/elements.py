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

import blockdiag.elements


class DiagramNode(blockdiag.elements.DiagramNode):
    pass


class FieldItem(blockdiag.elements.DiagramNode):
    shape = '_packet_node'
    desctable = ['number', 'label', 'description']
    attrname = dict(number='Seq', label='Name', description='Description')

    def __init__(self, begin, end, label):
        super(FieldItem, self).__init__(None)
        self.label = label
        self.separated_right = False
        self.separated_left = False

        if begin is None:
            self.number = None
            self.colwidth = 1
        elif end is None:
            self.number = int(begin)
            self.colwidth = 1
        else:
            self.number = int(begin)
            self.colwidth = int(end) - int(begin) + 1

            if self.colwidth <= 0:
                msg = ("Invalid field size definition: %d-%d: %s\n" %
                       (begin, end, label))
                raise AttributeError(msg)

    def set_height(self, value):
        self.colheight = int(value)

    def set_len(self, value):
        self.colwidth = int(value)


class Diagram(blockdiag.elements.Diagram):
    _DiagramNode = FieldItem

    def __init__(self):
        super(Diagram, self).__init__()
        self.colwidth = 16
        self.scale_interval = None
        self.scale_direction = "left_to_right"

        self.int_attrs.append('scale_interval')

    @property
    def fields(self):
        return self.nodes

    def set_scale_direction(self, value):
        value = value.lower()
        if value in ('ltr', 'left_to_right'):
            self.scale_direction = 'left_to_right'
        elif value in ('rtl', 'right_to_left'):
            self.scale_direction = 'right_to_left'
        else:
            msg = "unknown scale_direction: %s\n" % value
            raise AttributeError(msg)
