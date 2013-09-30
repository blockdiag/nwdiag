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
from docutils import nodes
from docutils.parsers import rst
from rackdiag import parser
from rackdiag.elements import RackItem
from rackdiag.builder import ScreenNodeBuilder
from rackdiag.drawer import DiagramDraw
from rackdiag.utils.rst.nodes import rackdiag
from blockdiag.utils.rst import directives
from blockdiag.utils.compat import u, cmp_to_key


directive_options_default = dict(format='PNG',
                                 antialias=False,
                                 fontpath=None,
                                 outputdir=None,
                                 nodoctype=False,
                                 noviewbox=False,
                                 inline_svg=False,
                                 ignore_pil=False)
directive_options = {}


class RackdiagDirectiveBase(directives.BlockdiagDirectiveBase):
    """ Directive to insert arbitrary dot markup. """
    name = "rackdiag"
    node_class = rackdiag


class RackdiagDirective(directives.BlockdiagDirective):
    name = "rackdiag"
    node_class = rackdiag

    @property
    def global_options(self):
        return directive_options

    def node2diagram(self, node):
        tree = parser.parse_string(node['code'])
        return ScreenNodeBuilder.build(tree)

    def node2image(self, node, diagram):
        options = node['options']
        filename = self.image_filename(node)
        fontmap = self.create_fontmap()
        _format = self.global_options['format'].lower()

        if _format == 'svg' and self.global_options['inline_svg'] is True:
            filename = None

        kwargs = dict(self.global_options)
        del kwargs['format']
        drawer = DiagramDraw(_format, diagram, filename,
                             fontmap=fontmap, **kwargs)

        if filename is None or not os.path.isfile(filename):
            drawer.draw()
            content = drawer.save(None)

            if _format == 'svg' and self.global_options['inline_svg'] is True:
                size = drawer.pagesize()
                if 'maxwidth' in options and options['maxwidth'] < size[0]:
                    ratio = float(options['maxwidth']) / size[0]
                    new_size = (options['maxwidth'], int(size[1] * ratio))
                    content = drawer.save(new_size)

                return nodes.raw('', content, format='html')

        size = drawer.pagesize()
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
        widths = [25] + [50] * (len(RackItem.desctable) - 1)
        headers = [RackItem.attrname[name] for name in RackItem.desctable]

        descriptions = [n.to_desctable() for n in nodes()]
        descriptions.sort(key=cmp_to_key(directives.cmp_node_number))

        # records for total
        total = ['-', 'Total'] + [''] * (len(RackItem.desctable) - 2)
        total[2] = u("%dU") % sum(n.colheight for n in nodes() if n.colheight)
        total[3] = u("%.1fA") % sum(n.ampere for n in nodes() if n.ampere)
        total[4] = u("%.1fkg") % sum(n.weight for n in nodes() if n.weight)
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
    for key, value in directive_options_default.items():
        directive_options[key] = kwargs.get(key, value)

    rst.directives.register_directive("rackdiag", RackdiagDirective)
