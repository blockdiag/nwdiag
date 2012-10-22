# -*- coding: utf-8 -*-
#  Copyright 2012 Takeshi KOMIYA
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
from docutils import nodes
from docutils.parsers import rst
from packetdiag import parser
from packetdiag.elements import FieldItem
from packetdiag.builder import ScreenNodeBuilder
from packetdiag.drawer import DiagramDraw
from blockdiag.utils.rst import directives


directive_options_default = dict(format='PNG',
                                 antialias=False,
                                 fontpath=None,
                                 outputdir=None,
                                 nodoctype=False,
                                 noviewbox=False,
                                 inline_svg=False,
                                 ignore_pil=False)
directive_options = {}


class packetdiag(nodes.General, nodes.Element):
    pass


class PacketdiagDirectiveBase(directives.BlockdiagDirectiveBase):
    """ Directive to insert arbitrary dot markup. """
    name = "packetdiag"
    node_class = packetdiag


class PacketdiagDirective(directives.BlockdiagDirective):
    name = "packetdiag"
    node_class = packetdiag

    @property
    def global_options(self):
        return directive_options

    def node2diagram(self, node):
        tree = parser.parse_string(node['code'])
        return ScreenNodeBuilder.build(tree)

    def node2image(self, node, diagram):
        filename = self.image_filename(node)
        fontpath = self.detectfont()
        format = self.global_options['format'].lower()

        if format == 'svg' and self.global_options['inline_svg'] is True:
            filename = None

        kwargs = dict(self.global_options)
        del kwargs['format']
        drawer = DiagramDraw(format, diagram, filename, **kwargs)

        if filename is None or not os.path.isfile(filename):
            drawer.draw()
            content = drawer.save(None)

            if format == 'svg' and self.global_options['inline_svg'] is True:
                return nodes.raw('', content.encode('utf-8'), format='html')

        size = drawer.pagesize()
        options = node['options']
        if 'maxwidth' in options and options['maxwidth'] < size[0]:
            ratio = float(options['maxwidth']) / size[0]
            thumb_size = (options['maxwidth'], size[1] * ratio)

            thumb_filename = self.image_filename(node, prefix='_thumb')
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
        nodes = diagram.traverse_nodes
        widths = [25] + [50] * (len(FieldItem.desctable) - 1)
        headers = [FieldItem.attrname[name] for name in FieldItem.desctable]

        descriptions = [n.to_desctable() for n in nodes()]
        descriptions.sort(directives.cmp_node_number)

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
    global directive_options, directive_options_default

    for key, value in directive_options_default.items():
        directive_options[key] = kwargs.get(key, value)

    rst.directives.register_directive("packetdiag", PacketdiagDirective)
