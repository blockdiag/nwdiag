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
from nwdiag import parser
from nwdiag.builder import ScreenNodeBuilder
from nwdiag.drawer import DiagramDraw
from blockdiag.utils.rst import directives


directive_options = dict(format='PNG',
                         antialias=False,
                         fontpath=None,
                         outputdir=None,
                         nodoctype=False,
                         noviewbox=False,
                         inline_svg=False)


class nwdiag(nodes.General, nodes.Element):
    pass


class NwdiagDirectiveBase(directives.BlockdiagDirectiveBase):
    """ Directive to insert arbitrary dot markup. """
    name = "nwdiag"
    node_class = nwdiag


class NwdiagDirective(directives.BlockdiagDirective):
    name = "nwdiag"
    node_class = nwdiag

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

        kwargs = dict(self.global_options)
        del kwargs['format']
        drawer = DiagramDraw(format, diagram, filename, **kwargs)

        if not os.path.isfile(filename):
            drawer.draw()
            if format == 'svg' and self.global_options['inline_svg'] is True:
                content = drawer.save(None)
                return nodes.raw('', content, format='html')
            else:
                drawer.save()

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


def setup(**kwargs):
    global directive_options

    directive_options['format'] = kwargs.get('format', 'PNG')
    directive_options['antialias'] = kwargs.get('antialias', False)
    directive_options['fontpath'] = kwargs.get('fontpath', None)
    directive_options['outputdir'] = kwargs.get('outputdir', None)
    directive_options['nodoctype'] = kwargs.get('nodoctype', False)
    directive_options['noviewbox'] = kwargs.get('noviewbox', False)
    directive_options['inline_svg'] = kwargs.get('inline_svg', False)

    rst.directives.register_directive("nwdiag", NwdiagDirective)
