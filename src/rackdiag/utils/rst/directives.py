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

import os
import codecs
from docutils import nodes
from docutils.parsers import rst
from rackdiag import diagparser
from rackdiag.builder import ScreenNodeBuilder
from rackdiag.DiagramDraw import DiagramDraw
from blockdiag.utils.rst import directives


format = 'PNG'
antialias = False
fontpath = None


class rackdiag(nodes.General, nodes.Element):
    pass


class RackdiagDirectiveBase(directives.BlockdiagDirectiveBase):
    """ Directive to insert arbitrary dot markup. """
    name = "rackdiag"
    node_class = rackdiag


class RackdiagDirective(directives.BlockdiagDirective):
    name = "rackdiag"
    node_class = rackdiag

    def node2diagram(self, node):
        tree = diagparser.parse_string(node['code'])
        return ScreenNodeBuilder.build(tree)

    def node2image(self, node, diagram):
        filename = self._filename(node)
        fontpath = self.detectfont()
        drawer = DiagramDraw(format, diagram, filename,
                             font=fontpath, antialias=antialias)

        if not os.path.isfile(filename):
            drawer.draw()
            drawer.save()

        size = drawer.pagesize()
        options = node['options']
        if 'maxwidth' in options and options['maxwidth'] < size[0]:
            ratio = float(options['maxwidth']) / size[0]
            thumb_size = (options['maxwidth'], size[1] * ratio)

            thumb_filename = self._filename(node, prefix='_thumb')
            if not os.path.isfile(thumb_filename):
                drawer.filename = thumb_filename
                drawer.draw()
                drawer.save(thumb_size)

            image = nodes.image(uri=thumb_filename, target=filename)
        else:
            image = nodes.image(uri=filename)

        if node['alt']:
            image['alt'] = node['alt']

        return image

    def description_table(self, diagram):
        descriptions = []
        widths = [25, 50, 50, 50, 50, 50]
        headers = ['No', 'Name', 'Height', 'Capacity', 'Weight', 'Description']
        nodes = diagram.traverse_nodes()

        for n in nodes:
            label = n.label or n.id
            units = u"%dU" % n.colheight
            ampere = n.ampere and (u"%.1fA" % n.ampere) or ''
            weight = n.weight and (u"%.1fkg" % n.weight) or ''

            record = [n.number, n.label, units, ampere, weight, n.description]
            descriptions.append(record)
        descriptions.sort(directives.cmp_node_number)

        # records for total
        total = ['-', 'Total', '', '', '', '']
        total[2] = u"%dU" % sum(n.colheight for n in nodes  if n.colheight)
        total[3] = u"%.1fA" % sum(n.ampere for n in nodes  if n.ampere)
        total[4] = u"%.1fkg" % sum(n.weight for n in nodes  if n.weight)
        descriptions.append(total)

        for i in range(len(headers) - 1, -1, -1):
            if any(desc[i] for desc in descriptions):
                pass
            else:
                widths.pop(i)
                headers.pop(i)
                for desc in descriptions:
                    desc.pop(i)

        return self._description_table(descriptions, widths, headers)


def setup(**kwargs):
    global format, antialias, fontpath
    format = kwargs.get('format', 'PNG')
    antialias = kwargs.get('antialias', False)
    fontpath = kwargs.get('fontpath', None)

    rst.directives.register_directive("rackdiag", RackdiagDirective)
